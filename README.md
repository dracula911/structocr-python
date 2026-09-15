# StructOCR Python SDK

Official Python client for the [StructOCR API](https://structocr.com/developers).

The SDK accepts a local JPG, PNG, WebP, or PDF path, plus in-memory `bytes`. It validates the decoded file locally, converts it to Base64, and sends JSON as `{"img": "..."}`. The REST API also supports multipart uploads; this SDK release keeps Base64 JSON as its default transport for backward compatibility.

## Install

```bash
pip install --upgrade structocr
```

Python 3.7+ is required.

## Quick start

```bash
export STRUCTOCR_API_KEY="YOUR_API_KEY"
```

```python
from structocr import StructOCR

client = StructOCR()
result = client.scan_passport("./passport.jpg")

if result.get("success"):
    data = result["data"]
    print(data.get("passport_number"))
    print(data.get("given_names"), data.get("surname"))
```

PDF paths work the same way:

```python
result = client.scan_invoice("./invoice.pdf")
```

FastAPI and other server frameworks can pass uploaded bytes without a temporary file:

```python
content = await upload.read()
result = client.scan_passport(content)
```

## Methods

```text
scan_passport(file)
scan_national_id(file)
scan_driver_license(file)
scan_invoice(file)
scan_receipt(file)
scan_vin(file)
scan_hin(file)
scan_container(file)
scan_license_plate(file)
scan_vehicle_registration(file)
scan_atm_cassette(file)
scan_weighbridge_ticket(file)
get_account_balance()
```

All document methods accept a local path or bytes. Supported decoded formats are JPG, PNG, WebP, and PDF, up to 4.5MB.

Receipt v2 provides a richer response. Enhanced accuracy requires v2 and costs 2 credits instead of the standard 1 credit:

```python
receipt = client.scan_receipt(
    "./receipt.jpg",
    response_version=2,
    accuracy="enhanced",
)
```

Weighbridge ticket example:

```python
result = client.scan_weighbridge_ticket("./weighbridge-ticket.jpg")
if result.get("success"):
    print(result["data"]["weights"])
    print(result["data"]["validation"])
```

## Configuration

```python
client = StructOCR(
    api_key="YOUR_API_KEY",
    base_url="https://api.structocr.com/v1",
    timeout=60,
)
```

See the [API documentation](https://structocr.com/developers) for endpoint-specific response schemas and error codes.

## Errors

API and network failures raise `StructOCRError`. Existing `except RuntimeError` code continues to work because `StructOCRError` extends `RuntimeError`.

```python
from structocr import StructOCRError

try:
    client.scan_passport("./passport.jpg")
except StructOCRError as error:
    print(error.status_code, error.code, error.retryable)
```

`retryable` is advisory only. The SDK does not automatically retry OCR requests because doing so without an idempotency key could charge a request twice.

## License

MIT
