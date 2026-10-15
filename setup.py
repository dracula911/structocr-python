from setuptools import setup, find_packages
from pathlib import Path


ROOT = Path(__file__).parent
VERSION = {}
exec((ROOT / "structocr" / "version.py").read_text(encoding="utf-8"), VERSION)

setup(
    name="structocr",
    version=VERSION["__version__"],
    description="Passport, ID card, driver license, VIN, invoice and receipt OCR: turn images and PDFs into structured JSON. Official StructOCR SDK for Python.",
    keywords=["ocr", "passport ocr", "mrz", "id card ocr", "driver license ocr", "pdf417", "vin ocr", "invoice ocr", "receipt ocr", "kyc", "document ai", "structocr"],
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    license="MIT",
    license_files=("LICENSE",),
    
    author="StructOCR Team",
    author_email="support@structocr.com",
    
    url="https://structocr.com", 
    
    project_urls={
        "Homepage": "https://structocr.com",
        "Documentation": "https://structocr.com/developers",
        "Get a free API key": "https://structocr.com/register?utm_source=pypi&utm_medium=project_urls&utm_campaign=sdk",
        "Source": "https://github.com/dracula911/structocr-python",
        "Tracker": "https://github.com/dracula911/structocr-python/issues",
    },

    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires='>=3.7',
)
