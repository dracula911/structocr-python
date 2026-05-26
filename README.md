# StructOCR Python SDK

[![PyPI version](https://badge.fury.io/py/structocr.svg)](https://badge.fury.io/py/structocr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**The official Python client for [StructOCR](https://structocr.com).**

StructOCR is a powerful API tailored for developers to extract structured data from complex documents and physical assets with high accuracy. This SDK helps you integrate **Passport OCR**, **National ID OCR**, **Driver License OCR**, **Invoice OCR**, **Receipt OCR**, **VIN OCR**, **HIN OCR**, and **Container OCR** into your Python applications in minutes.

👉 **[Get your Free API Key here](https://structocr.com)**

-----

## 🚀 What's New in 1.3.0

We've massively upgraded our Identity Verification engine! 
* **Hybrid VIZ + MRZ AI for National IDs**: The SDK now automatically cross-validates unstructured Visual Zone (VIZ) data against cryptographic Machine Readable Zone (MRZ) checksums (TD1/TD2) for zero hallucination. Raw MRZ lines are now accessible via `additional_fields`.
* *Previous marine & expense additions (Receipt OCR, HIN OCR, Container OCR) remain fully supported.*

Check out the [Quick Start](#quick-start) below to see how easy it is to use them!

-----

## Features

  - **Passport OCR API**: Instantly extract MRZ, name, DOB, and expiry date from passports of 200+ countries.
  - **National ID OCR**: Extract regional specific fields (CNP, CPF, NIN) and raw ICAO 9303 MRZ lines with hybrid validation.
  - **Driver License OCR**: Extract vehicle class, license number, and personal details.
  - **Invoice OCR**: Extract invoice number, currency, merchant, customer, and financial totals.
  - **Receipt OCR**: Extract merchants, dates, line items, taxes, and totals for expense management.
  - **VIN OCR**: Extract VIN (Vehicle Identification Number) from windshield or engine bay images.
  - **HIN OCR**: Validate and extract Hull Identification Numbers from marine vessels.
  - **Container OCR**: Extract shipping container numbers accurately from images.
  - **Secure & Fast**: Enterprise-grade encryption, SOC2 compliance, and sub-second response times with zero data retention.

## Installation

Install the package via pip:

```bash
pip install structocr
```

## Quick Start

### 1\. Initialize the Client

```python
from structocr import StructOCR

# Initialize with your API Key
client = StructOCR(api_key="sk_live_xxxxxxxx")
```

### 2\. Scan a Passport (Passport OCR)

```python
# Pass the path to the passport image file
result = client.scan_passport('./docs/passport_sample.jpg')

print(f"Name: {result['data']['name']}")
print(f"Passport Number: {result['data']['document_number']}")
```

### 3\. Scan Other Documents and Assets

```python
# National ID OCR
id_data = client.scan_national_id('./docs/id_card.png')

# Driver License OCR
license_data = client.scan_driver_license('./docs/license.jpg')

# Invoice OCR
invoice_data = client.scan_invoice('./docs/invoice.jpg')

# Receipt OCR (New in 1.2.0)
receipt_data = client.scan_receipt('./docs/receipt.jpg')

# VIN OCR
vin_data = client.scan_vin('./docs/vin.jpg')

# HIN OCR (New in 1.2.0)
hin_data = client.scan_hin('./docs/boat_hin.jpg')

# Container OCR
container_data = client.scan_container('./docs/container.jpg')
```

## Documentation

For full API documentation, response examples, and error codes, please visit the [StructOCR Developer Docs](https://www.structocr.com/developers?ref=github).

## Requirements

  * Python 3.7+
  * `requests` library

## License

MIT License. See [LICENSE](https://opensource.org/licenses/MIT) for details.