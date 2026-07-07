from setuptools import setup, find_packages

setup(
    name="structocr",
    version="1.4.0",
    description="The official Python SDK for StructOCR API - Passport, ID card, Driver License OCR, Invoice, Receipts, VIN, HIN, License plate, and Container OCR.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    
    author="StructOCR Team",
    author_email="support@structocr.com",
    
    url="https://structocr.com", 
    
    project_urls={
        "Homepage": "https://structocr.com",
        "Documentation": "https://structocr.com/developers", 
        "Source": "https://github.com/structocr/structocr-python",
        "Tracker": "https://github.com/structocr/structocr-python/issues", 
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
    python_requires='>=3.6',
)