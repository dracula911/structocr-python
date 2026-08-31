from setuptools import setup, find_packages
from pathlib import Path


ROOT = Path(__file__).parent

setup(
    name="structocr",
    version="1.5.0",
    description="Official Python SDK for StructOCR Base64 document APIs, including images, PDFs, and account balance.",
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
