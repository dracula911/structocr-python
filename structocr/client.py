import base64
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests


FileInput = Union[str, os.PathLike, bytes, bytearray, memoryview]
MAX_FILE_SIZE = int(4.5 * 1024 * 1024)
SUPPORTED_FORMATS = "JPG, PNG, WebP, and PDF"


class StructOCR:
    """Official Python client for the StructOCR Base64 JSON API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.structocr.com/v1",
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("STRUCTOCR_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Get one at https://structocr.com")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "StructOCR-Python/1.5.0",
        })

    @staticmethod
    def _read_file(file: FileInput) -> bytes:
        if isinstance(file, (bytes, bytearray, memoryview)):
            content = bytes(file)
        else:
            path = Path(file)
            if not path.is_file():
                raise FileNotFoundError(f"File not found: {path}")
            content = path.read_bytes()

        if not content:
            raise ValueError("File is empty")
        if len(content) > MAX_FILE_SIZE:
            raise ValueError("File exceeds the maximum allowed size of 4.5MB")
        if StructOCR._detect_mime(content) is None:
            raise ValueError(f"Unsupported file format. Supported formats: {SUPPORTED_FORMATS}")
        return content

    @staticmethod
    def _detect_mime(content: bytes) -> Optional[str]:
        if content.startswith(b"%PDF"):
            return "application/pdf"
        if content.startswith(b"\xff\xd8\xff"):
            return "image/jpeg"
        if content.startswith(b"\x89PNG\r\n\x1a\n"):
            return "image/png"
        if len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
            return "image/webp"
        return None

    def _post_image(self, endpoint: str, file: FileInput) -> Dict[str, Any]:
        """Read a local file or bytes and send it as Base64 JSON in ``img``."""
        content = self._read_file(file)
        payload = {"img": base64.b64encode(content).decode("ascii")}

        try:
            response = self.session.post(
                f"{self.base_url}/{endpoint}",
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            raise RuntimeError(f"API request failed: {error}") from error

    def get_account_balance(self) -> Dict[str, Any]:
        """Return account-level and current-key usage from ``/account/balance``."""
        try:
            response = self.session.get(
                f"{self.base_url}/account/balance",
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            raise RuntimeError(f"API request failed: {error}") from error

    def scan_passport(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("passport", file)

    def scan_national_id(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("national-id", file)

    def scan_driver_license(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("driver-license", file)

    def scan_invoice(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("invoice", file)

    def scan_vin(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("vin", file)

    def scan_container(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("container", file)

    def scan_hin(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("hin", file)

    def scan_receipt(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("receipt", file)

    def scan_license_plate(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("license-plate", file)

    def scan_vehicle_registration(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("vehicle-registration", file)

    def scan_atm_cassette(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("atm-cassette", file)
