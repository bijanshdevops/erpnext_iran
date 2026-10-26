"""Client for the Tax Organization's Moadian API (v2), for taxpayers sending directly.

Flow: GET nonce -> token (JWS over {nonce, clientId} signed with the taxpayer's key, certificate in
x5c) -> server-information (the organization's public key) -> each invoice signed as a JWS, then
encrypted as a JWE (RSA-OAEP-256 + A256GCM) and POSTed to invoice -> inquiry-by-reference-id.
Independent of Frappe; `session` is anything with requests-style get() and post().
"""

import base64
import datetime
import json
import os
import uuid

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PRODUCTION_URL = "https://tp.tax.gov.ir/requestsmanager/api/v2/"


class MoadianError(Exception):
	pass


def b64url(data):
	if isinstance(data, str):
		data = data.encode()
	return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_decode(text):
	return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def _json(value):
	return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def certificate_b64(certificate_pem):
	"""The certificate as base64 DER, for the x5c header."""
	cert = x509.load_pem_x509_certificate(certificate_pem.encode() if isinstance(certificate_pem, str) else certificate_pem)
	return base64.b64encode(cert.public_bytes(serialization.Encoding.DER)).decode()


def sign_jws(payload, private_key, certificate, now=None):
	"""Compact JWS (RS256) with the header fields the organization requires (x5c, sigT, crit)."""
	now = now or datetime.datetime.now(datetime.timezone.utc)
	header = {
		"alg": "RS256",
		"x5c": [certificate],
		"sigT": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
		"typ": "jose",
		"crit": ["sigT"],
		"cty": "text/plain",
	}
	signing_input = f"{b64url(_json(header))}.{b64url(payload)}"
	signature = private_key.sign(signing_input.encode(), padding.PKCS1v15(), hashes.SHA256())
	return f"{signing_input}.{b64url(signature)}"


def load_public_key(key):
	"""The organization's key from server-information: base64 DER or PEM."""
	key = key.strip()
	if key.startswith("-----BEGIN"):
		return serialization.load_pem_public_key(key.encode())
	return serialization.load_der_public_key(base64.b64decode(key))


def encrypt_jwe(plaintext, public_key, kid):
	"""Compact JWE: RSA-OAEP-256 key wrap, A256GCM content encryption, header as AAD."""
	header = b64url(_json({"alg": "RSA-OAEP-256", "enc": "A256GCM", "kid": kid}))
	cek, iv = os.urandom(32), os.urandom(12)
	encrypted_key = public_key.encrypt(
		cek, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
	)
	sealed = AESGCM(cek).encrypt(iv, plaintext.encode(), header.encode())
	ciphertext, tag = sealed[:-16], sealed[-16:]
	return ".".join([header, b64url(encrypted_key), b64url(iv), b64url(ciphertext), b64url(tag)])


class MoadianClient:
	def __init__(self, memory_id, private_key_pem, certificate_pem, base_url=PRODUCTION_URL, session=None, timeout=30):
		self.memory_id = memory_id
		self.private_key = serialization.load_pem_private_key(
			private_key_pem.encode() if isinstance(private_key_pem, str) else private_key_pem, password=None
		)
		self.certificate = certificate_b64(certificate_pem)
		self.base_url = base_url.rstrip("/") + "/"
		self.timeout = timeout
		if session is None:
			import requests

			session = requests.Session()
		self.session = session

	# ---- HTTP
	def _request(self, method, path, token=None, **kwargs):
		headers = {"Accept": "*/*", "Content-Type": "application/json"}
		if token:
			headers["Authorization"] = f"Bearer {token}"
		response = getattr(self.session, method)(self.base_url + path, headers=headers, timeout=self.timeout, **kwargs)
		try:
			body = response.json()
		except ValueError:
			body = None
		if not 200 <= response.status_code < 300:
			raise MoadianError(f"{path}: HTTP {response.status_code} {body if body is not None else response.text}")
		return body

	# ---- authentication
	def nonce(self, time_to_live=30):
		return self._request("get", "nonce", params={"timeToLive": time_to_live})["nonce"]

	def token(self):
		payload = _json({"nonce": self.nonce(), "clientId": self.memory_id})
		return sign_jws(payload, self.private_key, self.certificate)

	# ---- API
	def server_information(self, token=None):
		return self._request("get", "server-information", token or self.token())

	def fiscal_information(self, token=None):
		return self._request("get", "fiscal-information", token or self.token(), params={"memoryId": self.memory_id})

	def send_invoices(self, invoices):
		"""Send invoice payloads (dicts); returns [{"uid", "referenceNumber", ...}] in the same order."""
		token = self.token()
		keys = (self.server_information(token) or {}).get("publicKeys") or []
		if not keys:
			raise MoadianError("server-information returned no public key")
		public_key, kid = load_public_key(keys[0]["key"]), keys[0]["id"]

		packets, uids = [], []
		for invoice in invoices:
			uid = str(uuid.uuid4())
			jws = sign_jws(_json(invoice), self.private_key, self.certificate)
			packets.append(
				{"header": {"requestTraceId": uid, "fiscalId": self.memory_id}, "payload": encrypt_jwe(jws, public_key, kid)}
			)
			uids.append(uid)
		response = self._request("post", "invoice", token, data=_json(packets).encode())
		by_uid = {row.get("uid"): row for row in (response or {}).get("result") or []}
		return [by_uid.get(uid, {"uid": uid}) for uid in uids]

	def inquiry_by_reference_ids(self, reference_ids):
		"""[{"referenceNumber", "status", "data": {"error": [...], "warning": [...], "success"}}]."""
		params = [("referenceIds", ref) for ref in reference_ids]
		return self._request("get", "inquiry-by-reference-id", self.token(), params=params) or []


def inquiry_outcome(result):
	"""(status, message) for one inquiry result: Accepted, Rejected or Sent (still being processed)."""
	status = (result.get("status") or "").upper()
	data = result.get("data") or {}
	errors = data.get("error") or []
	message = "\n".join(f"{e.get('code')}: {e.get('message')}" for e in errors)
	if status == "SUCCESS":
		warnings = data.get("warning") or []
		return "Accepted", "\n".join(f"{w.get('code')}: {w.get('message')}" for w in warnings)
	if status in ("FAILED", "TIMEOUT"):
		return "Rejected", message or status
	return "Sent", ""
