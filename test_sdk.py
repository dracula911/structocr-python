import base64
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from structocr import StructOCR
from structocr.client import MAX_FILE_SIZE


JPEG = b"\xff\xd8\xff\xe0test"
PDF = b"%PDF-1.7\ntest"


class StructOCRTests(unittest.TestCase):
    def setUp(self):
        self.client = StructOCR("test-key", base_url="https://example.test/v1")

    def test_path_is_sent_as_base64_json(self):
        response = Mock()
        response.json.return_value = {"success": True}
        response.raise_for_status.return_value = None
        self.client.session.post = Mock(return_value=response)

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image:
            image.write(JPEG)
            image.flush()
            result = self.client.scan_passport(image.name)

        self.assertEqual(result, {"success": True})
        self.client.session.post.assert_called_once_with(
            "https://example.test/v1/passport",
            json={"img": base64.b64encode(JPEG).decode("ascii")},
            timeout=30.0,
        )

    def test_bytes_and_pdf_are_supported(self):
        response = Mock()
        response.json.return_value = {"success": True}
        response.raise_for_status.return_value = None
        self.client.session.post = Mock(return_value=response)

        self.client.scan_invoice(PDF)

        payload = self.client.session.post.call_args.kwargs["json"]
        self.assertEqual(base64.b64decode(payload["img"]), PDF)

    def test_rejects_unknown_format(self):
        with self.assertRaisesRegex(ValueError, "Unsupported file format"):
            self.client.scan_passport(b"plain text")

    def test_rejects_decoded_file_over_limit(self):
        oversized = JPEG + b"0" * MAX_FILE_SIZE
        with self.assertRaisesRegex(ValueError, "4.5MB"):
            self.client.scan_passport(oversized)

    def test_new_endpoint_methods(self):
        self.client._post_image = Mock(return_value={"success": True})
        self.client.scan_vehicle_registration(JPEG)
        self.client.scan_atm_cassette(JPEG)
        self.assertEqual(self.client._post_image.call_args_list[0].args[0], "vehicle-registration")
        self.assertEqual(self.client._post_image.call_args_list[1].args[0], "atm-cassette")

    def test_balance_uses_get_without_body(self):
        response = Mock()
        response.json.return_value = {"account": {"credits_remaining": 200}}
        response.raise_for_status.return_value = None
        self.client.session.get = Mock(return_value=response)

        result = self.client.get_account_balance()

        self.assertEqual(result["account"]["credits_remaining"], 200)
        self.client.session.get.assert_called_once_with(
            "https://example.test/v1/account/balance",
            timeout=30.0,
        )

    def test_reads_canonical_environment_variable(self):
        with patch.dict(os.environ, {"STRUCTOCR_API_KEY": "env-key"}):
            client = StructOCR()
        self.assertEqual(client.api_key, "env-key")


if __name__ == "__main__":
    unittest.main()
