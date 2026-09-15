import base64
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import requests

from .version import __version__


FileInput = Union[str, os.PathLike, bytes, bytearray, memoryview]
MAX_FILE_SIZE = int(4.5 * 1024 * 1024)
SUPPORTED_FORMATS = "JPG, PNG, WebP, and PDF"
RETRYABLE_STATUS_CODES = {429, 502, 503, 504}


class StructOCRError(RuntimeError):
    """Structured SDK error for API, network, and client failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        code: Optional[str] = None,
        details: Any = None,
        retryable: bool = False,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.details = details
        self.retryable = retryable


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
            "User-Agent": f"StructOCR-Python/{__version__}",
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

    @staticmethod
    def _response_data(response: requests.Response) -> Dict[str, Any]:
        try:
            data = response.json()
        except ValueError as error:
            raise StructOCRError(
                "StructOCR API returned an invalid JSON response",
                status_code=getattr(response, "status_code", None),
                code="INVALID_RESPONSE",
            ) from error
        if not isinstance(data, dict):
            raise StructOCRError(
                "StructOCR API returned an invalid response object",
                status_code=getattr(response, "status_code", None),
                code="INVALID_RESPONSE",
                details=data,
            )
        return data

    @staticmethod
    def _raise_api_error(response: requests.Response, error: Exception) -> None:
        try:
            details = response.json()
        except ValueError:
            details = None
        status = getattr(response, "status_code", None)
        status = status if isinstance(status, int) else None
        code = None
        message = None
        if isinstance(details, dict):
            code = details.get("code") or details.get("error")
            message = details.get("message")
        if not message:
            message = f"StructOCR API request failed with HTTP {status or 'unknown'}"
        raise StructOCRError(
            message,
            status_code=status,
            code=code,
            details=details,
            retryable=status in RETRYABLE_STATUS_CODES,
        ) from error

    def _post_image(
        self,
        endpoint: str,
        file: FileInput,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Read a local file or bytes and send it as Base64 JSON in ``img``."""
        content = self._read_file(file)
        payload = {"img": base64.b64encode(content).decode("ascii")}

        try:
            request_kwargs: Dict[str, Any] = {"json": payload, "timeout": self.timeout}
            if params is not None:
                request_kwargs["params"] = params
            response = self.session.post(f"{self.base_url}/{endpoint}", **request_kwargs)
        except requests.exceptions.RequestException as error:
            raise StructOCRError(
                f"Network error while calling StructOCR API: {error}",
                code="NETWORK_ERROR",
                retryable=True,
            ) from error
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            self._raise_api_error(response, error)
        return self._response_data(response)

    def get_account_balance(self) -> Dict[str, Any]:
        """Return account-level and current-key usage from ``/account/balance``."""
        try:
            response = self.session.get(
                f"{self.base_url}/account/balance",
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as error:
            raise StructOCRError(
                f"Network error while calling StructOCR API: {error}",
                code="NETWORK_ERROR",
                retryable=True,
            ) from error
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            self._raise_api_error(response, error)
        return self._response_data(response)

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

    def scan_receipt(
        self,
        file: FileInput,
        response_version: int = 1,
        accuracy: str = "standard",
    ) -> Dict[str, Any]:
        if response_version not in (1, 2):
            raise StructOCRError("response_version must be 1 or 2", code="INVALID_OPTIONS")
        if accuracy not in ("standard", "enhanced"):
            raise StructOCRError(
                'accuracy must be "standard" or "enhanced"',
                code="INVALID_OPTIONS",
            )
        if accuracy == "enhanced" and response_version != 2:
            raise StructOCRError(
                "Enhanced accuracy requires response_version=2",
                code="INVALID_OPTIONS",
            )
        if response_version == 1 and accuracy == "standard":
            return self._post_image("receipt", file)
        return self._post_image(
            "receipt",
            file,
            params={"response_version": response_version, "accuracy": accuracy},
        )

    def scan_license_plate(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("license-plate", file)

    def scan_vehicle_registration(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("vehicle-registration", file)

    def scan_atm_cassette(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("atm-cassette", file)

    def scan_weighbridge_ticket(self, file: FileInput) -> Dict[str, Any]:
        return self._post_image("weighbridge-ticket", file)
