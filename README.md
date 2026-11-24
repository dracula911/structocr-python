# StructOCR Python SDK

Official Python client for the [StructOCR API](https://structocr.com/developers?utm_source=pypi&utm_medium=readme&utm_campaign=sdk).

Extract validated, structured JSON from 19 document types — spanning identity & KYC (passports, travel visas, proof of address, national IDs, driver licenses, PDF417 barcodes, health insurance cards), vehicles & insurance (VIN, VIN Pro vehicle decode, license plates, registrations, auto insurance cards), finance (invoices, receipts), and logistics (bills of lading, shipping containers, weighbridge tickets, ATM cassettes, boat HINs). One method call per document, zero template training.

The SDK accepts a local JPG, PNG, WebP, or PDF path, plus in-memory `bytes`. It validates the decoded file locally, converts it to Base64, and sends JSON as `{"img": "..."}`. The REST API also supports multipart uploads; this SDK release keeps Base64 JSON as its default transport for backward compatibility.

## Get a free API key

1. [Create an account](https://structocr.com/register?utm_source=pypi&utm_medium=readme&utm_campaign=sdk). New accounts get **200 free credits**, enough for 100 two-credit document scans, and no credit card is needed.
2. Copy your key from **API Keys** in the dashboard.
3. Optionally test any of the 19 endpoints on a sample image in the [Playground](https://structocr.com/dashboard/playground?utm_source=pypi&utm_medium=readme&utm_campaign=sdk) before you write code.

Not ready to sign up? Try documents directly in your browser on a sample image or your own file, no account needed: use the **Try it** links in the table below.

After the free credits, packs start at $5 for 500 credits. There is no subscription and credits do not expire. See [pricing](https://structocr.com/pricing?utm_source=pypi&utm_medium=readme&utm_campaign=sdk).

## Supported documents

| Document | Method | Credits per scan | Try it |
| --- | --- | --- | --- |
| Passport | `scan_passport` | 2 | [Try it](https://structocr.com/products/passport-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Driver license (front) | `scan_driver_license` | 2 | [Try it](https://structocr.com/products/driver-license-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| US/Canada driver license PDF417 barcode | `scan_driver_license_pdf417` | 2 | [Try it](https://structocr.com/tools/driver-license-pdf417-scanner?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try) |
| National ID card | `scan_national_id` | 2 | [Try it](https://structocr.com/products/national-id-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Health insurance card *(New)* | `scan_health_card` | 2 | [Try it](https://structocr.com/products/health-card-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Proof of Address *(New)* | `scan_proof_of_address` | 2 | [Try it](https://structocr.com/products/proof-of-address-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Travel visa (MRV-A/B & eVisa) *(New)* | `scan_visa` | 2 | [Try it](https://structocr.com/products/visa-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| VIN | `scan_vin` | 1 | [Try it](https://structocr.com/products/vin-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| VIN Pro (VIN + vehicle details) *(New)* | `scan_vin_pro` | 2 | |
| License plate | `scan_license_plate` | 1 | [Try it](https://structocr.com/products/license-plate-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Vehicle registration | `scan_vehicle_registration` | 2 | [Try it](https://structocr.com/products/vehicle-registration-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Auto insurance card *(New)* | `scan_auto_insurance` | 2 | [Try it](https://structocr.com/products/auto-insurance-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Invoice | `scan_invoice` | 3 | [Try it](https://structocr.com/products/invoice-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Receipt | `scan_receipt` | 1 | [Try it](https://structocr.com/products/receipt-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Shipping container (ISO 6346) | `scan_container` | 1 | [Try it](https://structocr.com/products/container-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Bill of Lading & freight *(New)* | `scan_bill_of_lading` | 3 | [Try it](https://structocr.com/products/bill-of-lading-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| Weighbridge ticket | `scan_weighbridge_ticket` | 2 | [Try it](https://structocr.com/products/weighbridge-ticket-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |
| ATM cassette | `scan_atm_cassette` | 1 | |
| HIN (boat hull number) | `scan_hin` | 1 | [Try it](https://structocr.com/products/hin-ocr?utm_source=pypi&utm_medium=readme&utm_campaign=sdk_try#live-demo) |

The receipt endpoint's optional enhanced mode costs 2 credits. Only successful requests are charged.

## What's new in v1.8.0

Added native SDK methods for all six newly launched StructOCR endpoints:

- **`scan_proof_of_address(file)`** (`POST /v1/proof-of-address`, 2 credits) — Utility bills, bank statements, tax notices, and leases with 90/180-day freshness and PO Box checks.
- **`scan_visa(file)`** (`POST /v1/visa`, 2 credits) — Passport visa stickers (ICAO 9303 MRV-A 2×44 & MRV-B 2×36 check-digit verification) and global eVisa PDFs.
- **`scan_bill_of_lading(file)`** (`POST /v1/bill-of-lading`, 3 credits) — Ocean/road Bills of Lading, Packing Lists, Air Waybills (IATA Mod-7 validation), Commercial Invoices, and signed PODs with ISO 6346 container checks and cargo weight reconciliation.
- **`scan_health_card(file)`** (`POST /v1/health-card`, 2 credits) — US health insurance cards (Member ID, Group, RxBIN/RxPCN/RxGRP, copays), GCC/Canada/India/Brazil medical cards, and EU Tessera Sanitaria/EHIC, including 2-page front+back PDFs.
- **`scan_auto_insurance(file)`** (`POST /v1/auto-insurance`, 2 credits) — US ACORD 50 / state proof of insurance and Canadian Pink Cards with NAIC, policy date, and VIN check-digit validation.
- **`scan_vin_pro(file)`** (`POST /v1/vin-pro`, 2 credits) — VIN OCR with ISO 3779 check-digit validation plus decoded vehicle year, make, model, trim, engine, and body class.

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

A passport scan returns JSON like this (fictional sample document):

```json
{
  "success": true,
  "data": {
    "type": "passport",
    "country_code": "UTO",
    "nationality": "UTOPIAN",
    "passport_number": "X4R7T2K9P",
    "surname": "MORGAN",
    "given_names": "OLIVIA ROSE",
    "sex": "F",
    "date_of_birth": "1990-03-14",
    "place_of_birth": "ZENITH CITY",
    "date_of_issue": "2024-07-16",
    "date_of_expiry": "2034-07-15",
    "place_of_issue": null
  }
}
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
scan_driver_license_pdf417(file)
scan_health_card(file)
scan_proof_of_address(file)
scan_visa(file)
scan_vin(file)
scan_vin_pro(file)
scan_license_plate(file)
scan_vehicle_registration(file)
scan_auto_insurance(file)
scan_invoice(file)
scan_receipt(file)
scan_container(file)
scan_bill_of_lading(file)
scan_weighbridge_ticket(file)
scan_atm_cassette(file)
scan_hin(file)
get_account_balance()
```

All document methods accept a local path or bytes, up to 4.5MB. Most methods support JPG, PNG, WebP, and PDF. `scan_driver_license_pdf417` accepts JPG, PNG, and WebP only.

The Receipt endpoint returns v2 by default. Enhanced accuracy costs 2 credits instead of the standard 1 credit and is enabled with the `accuracy` parameter:

```python
receipt = client.scan_receipt(
    "./receipt.jpg",
    accuracy="enhanced",
)
```

`response_version=2` remains accepted for compatibility but is not required. Receipt v1 is retired.

Proof of Address example:

```python
poa = client.scan_proof_of_address("./utility-bill.pdf")
if poa.get("success"):
    print(poa["data"]["address"], poa["data"]["validation"]["is_within_90_days"])
```

Travel Visa example:

```python
visa = client.scan_visa("./visa-sticker.jpg")
if visa.get("success"):
    print(visa["data"]["visa_number"], visa["data"]["validation"]["mrz_checksum_valid"])
```

Bill of Lading & freight example:

```python
bol = client.scan_bill_of_lading("./bill-of-lading.pdf")
if bol.get("success"):
    print(bol["data"]["document_type"], bol["data"]["containers"], bol["data"]["validation"])
```

US driver license PDF417 example:

```python
result = client.scan_driver_license_pdf417("./license-back.jpg")
if result.get("success"):
    print(result["data"]["document_number"])
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

See the [API documentation](https://structocr.com/developers?utm_source=pypi&utm_medium=readme&utm_campaign=sdk) for endpoint-specific response schemas and error codes.

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
