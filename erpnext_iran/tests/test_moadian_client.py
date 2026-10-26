"""The Moadian client against the mock server: real signatures, real encryption."""

import json
import unittest

try:
	from erpnext_iran.moadian.client import MoadianClient, MoadianError, b64url_decode, inquiry_outcome
	from erpnext_iran.tests.moadian_mock import MockMoadianServer, make_taxpayer_keys
except ImportError:  # cryptography not installed
	raise unittest.SkipTest("cryptography is not installed") from None

MEMORY_ID = "A1B2C3"
VALID = {"header": {"taxid": "A1B2C304E2B000000001E7", "tins": "14000000000"}, "body": [{"sstid": "1"}]}
INVALID = {"header": {"taxid": "SHORT", "tins": ""}, "body": []}


class TestMoadianClient(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.key_pem, cls.cert_pem = make_taxpayer_keys()

	def client(self, server, key_pem=None, cert_pem=None, memory_id=MEMORY_ID):
		return MoadianClient(memory_id, key_pem or self.key_pem, cert_pem or self.cert_pem,
							 base_url="https://mock.test/requestsmanager/api/v2/", session=server)  # fmt: skip

	def test_send_and_inquire(self):
		server = MockMoadianServer(MEMORY_ID)
		client = self.client(server)
		results = client.send_invoices([VALID, INVALID])
		self.assertEqual(len(results), 2)
		references = [r["referenceNumber"] for r in results]
		self.assertTrue(all(references))
		# the server decrypted and verified exactly what was sent
		self.assertEqual(server.invoices[references[0]]["invoice"], VALID)

		outcomes = {r["referenceNumber"]: inquiry_outcome(r) for r in client.inquiry_by_reference_ids(references)}
		self.assertEqual(outcomes[references[0]], ("Accepted", ""))
		status, message = outcomes[references[1]]
		self.assertEqual(status, "Rejected")
		self.assertIn("0100", message)
		self.assertIn("شماره مالیاتی نامعتبر است", message)

	def test_fiscal_information(self):
		info = self.client(MockMoadianServer(MEMORY_ID)).fiscal_information()
		self.assertEqual(info["memoryId"], MEMORY_ID)

	def test_key_not_matching_certificate_is_refused(self):
		other_key, _cert = make_taxpayer_keys("Someone Else")
		with self.assertRaises(MoadianError) as e:
			self.client(MockMoadianServer(MEMORY_ID), key_pem=other_key).fiscal_information()
		self.assertIn("401", str(e.exception))

	def test_wrong_memory_id_is_refused(self):
		with self.assertRaises(MoadianError):
			self.client(MockMoadianServer(MEMORY_ID), memory_id="ZZZZZZ").fiscal_information()

	def test_token_header(self):
		server = MockMoadianServer(MEMORY_ID)
		header = json.loads(b64url_decode(self.client(server).token().split(".")[0]))
		self.assertEqual(header["alg"], "RS256")
		self.assertEqual(header["crit"], ["sigT"])
		self.assertRegex(header["sigT"], r"^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$")
		self.assertEqual(len(header["x5c"]), 1)

	def test_inquiry_outcome(self):
		self.assertEqual(inquiry_outcome({"status": "PENDING"}), ("Sent", ""))
		self.assertEqual(inquiry_outcome({"status": "IN_PROGRESS"}), ("Sent", ""))
		self.assertEqual(inquiry_outcome({"status": "TIMEOUT", "data": {}}), ("Rejected", "TIMEOUT"))
		self.assertEqual(
			inquiry_outcome({"status": "SUCCESS", "data": {"warning": [{"code": "W1", "message": "x"}]}}),
			("Accepted", "W1: x"),
		)
