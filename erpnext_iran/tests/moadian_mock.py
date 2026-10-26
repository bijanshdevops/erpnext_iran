"""In-process stand-in for the Tax Organization's Moadian API, for tests.

It plays the server side of the protocol strictly: tokens must be JWS signatures by the
certificate in x5c over a nonce it issued, invoice packets must decrypt with its private key
and carry a valid JWS. Invoices are then accepted or rejected by a few schema checks.
"""

import base64
import datetime
import json
import os
import uuid
from urllib.parse import urlparse

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.x509.oid import NameOID

from erpnext_iran.moadian.client import b64url, b64url_decode

KID = "mock-key-1"


def make_taxpayer_keys(common_name="Test Taxpayer"):
	"""(private key PEM, self-signed certificate PEM), like the files a taxpayer gets."""
	key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
	name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
	now = datetime.datetime.now(datetime.timezone.utc)
	cert = (
		x509.CertificateBuilder()
		.subject_name(name)
		.issuer_name(name)
		.public_key(key.public_key())
		.serial_number(x509.random_serial_number())
		.not_valid_before(now - datetime.timedelta(days=1))
		.not_valid_after(now + datetime.timedelta(days=365))
		.sign(key, hashes.SHA256())
	)
	key_pem = key.private_bytes(
		serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()
	).decode()
	return key_pem, cert.public_bytes(serialization.Encoding.PEM).decode()


class Response:
	def __init__(self, status_code, body):
		self.status_code = status_code
		self._body = body
		self.text = json.dumps(body)

	def json(self):
		return self._body


class MockMoadianServer:
	def __init__(self, memory_id):
		self.memory_id = memory_id
		self.key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
		self.nonces = set()
		self.invoices = {}  # reference number -> {"invoice", "status", "errors"}
		self.calls = []

	# ---- requests-style session
	def get(self, url, headers=None, params=None, timeout=None):
		return self._handle("GET", url, headers or {}, params, None)

	def post(self, url, headers=None, data=None, timeout=None):
		return self._handle("POST", url, headers or {}, None, data)

	def _handle(self, method, url, headers, params, data):
		path = urlparse(url).path.rstrip("/").rsplit("/", 1)[-1]
		self.calls.append((method, path))
		if path == "nonce":
			nonce = str(uuid.uuid4())
			self.nonces.add(nonce)
			return Response(200, {"nonce": nonce, "expDate": 0})
		try:
			self._authenticate(headers.get("Authorization", ""))
		except Exception as e:
			return Response(401, {"error": f"unauthorized: {e}"})
		if path == "server-information":
			der = self.key.public_key().public_bytes(
				serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo
			)
			return Response(200, {"serverTime": 0, "publicKeys": [
				{"key": base64.b64encode(der).decode(), "id": KID, "algorithm": "RSA", "purpose": 1}]})  # fmt: skip
		if path == "fiscal-information":
			return Response(200, {"nameTrade": "شرکت آزمایشی", "fiscalStatus": "ACTIVE", "memoryId": self.memory_id})
		if path == "invoice" and method == "POST":
			return self._receive(json.loads(data))
		if path == "inquiry-by-reference-id":
			refs = [value for key, value in params if key == "referenceIds"]
			return Response(200, [self._inquiry(ref) for ref in refs if ref in self.invoices])
		return Response(404, {"error": path})

	# ---- protocol checks
	def _verify_jws(self, jws):
		header_b64, payload_b64, signature_b64 = jws.split(".")
		header = json.loads(b64url_decode(header_b64))
		assert header["alg"] == "RS256" and header["crit"] == ["sigT"] and header["sigT"], header
		cert = x509.load_der_x509_certificate(base64.b64decode(header["x5c"][0]))
		cert.public_key().verify(
			b64url_decode(signature_b64), f"{header_b64}.{payload_b64}".encode(), padding.PKCS1v15(), hashes.SHA256()
		)
		return b64url_decode(payload_b64).decode()

	def _authenticate(self, authorization):
		assert authorization.startswith("Bearer "), "no bearer token"
		payload = json.loads(self._verify_jws(authorization[len("Bearer ") :]))
		assert payload["nonce"] in self.nonces, "unknown nonce"
		assert payload["clientId"] == self.memory_id, "wrong clientId"

	def _decrypt(self, jwe):
		header_b64, key_b64, iv_b64, ciphertext_b64, tag_b64 = jwe.split(".")
		header = json.loads(b64url_decode(header_b64))
		assert header == {"alg": "RSA-OAEP-256", "enc": "A256GCM", "kid": KID}, header
		cek = self.key.decrypt(
			b64url_decode(key_b64),
			padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
		)
		plain = AESGCM(cek).decrypt(
			b64url_decode(iv_b64), b64url_decode(ciphertext_b64) + b64url_decode(tag_b64), header_b64.encode()
		)
		return plain.decode()

	def _receive(self, packets):
		result = []
		for packet in packets:
			assert packet["header"]["fiscalId"] == self.memory_id
			invoice = json.loads(self._verify_jws(self._decrypt(packet["payload"])))
			reference = str(uuid.uuid4())
			errors = self.check_invoice(invoice)
			self.invoices[reference] = {"invoice": invoice, "status": "FAILED" if errors else "SUCCESS", "errors": errors}
			result.append({"uid": packet["header"]["requestTraceId"], "packetType": "INVOICE.V01",
						   "referenceNumber": reference, "data": None})  # fmt: skip
		return Response(200, {"timestamp": 0, "result": result})

	@staticmethod
	def check_invoice(invoice):
		header, body = invoice.get("header") or {}, invoice.get("body") or []
		errors = []
		if len(str(header.get("taxid") or "")) != 22:
			errors.append({"code": "0100", "message": "شماره مالیاتی نامعتبر است", "errorType": "ERROR"})
		if not header.get("tins"):
			errors.append({"code": "0101", "message": "شناسه مالیاتی فروشنده وارد نشده است", "errorType": "ERROR"})
		if not body:
			errors.append({"code": "0102", "message": "صورتحساب ردیف کالا ندارد", "errorType": "ERROR"})
		return errors

	def _inquiry(self, reference):
		stored = self.invoices[reference]
		return {
			"referenceNumber": reference,
			"uid": None,
			"status": stored["status"],
			"packetType": "INVOICE.V01",
			"fiscalId": self.memory_id,
			"data": {"error": stored["errors"], "warning": [], "success": not stored["errors"]},
		}

	def install_keys(self, directory):
		"""Write a taxpayer key and certificate to directory; returns their paths."""
		key_pem, cert_pem = make_taxpayer_keys()
		paths = (os.path.join(directory, "moadian-key.pem"), os.path.join(directory, "moadian-cert.pem"))
		for path, content in zip(paths, (key_pem, cert_pem)):
			with open(path, "w") as f:
				f.write(content)
		return paths
