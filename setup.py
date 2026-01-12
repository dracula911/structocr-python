from setuptools import setup, find_packages

setup(
    name="structocr",
    version="1.0.0",
    description="The official Python SDK for StructOCR API - Passport, ID, and Driver License OCR.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="StructOCR Team",
    author_email="support@structocr.com",
    url="https://github.com/structocr/structocr-python", # 记得换成你未来的 github 地址
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Image Recognition", # 这是一个很好的分类标签
    ],
    python_requires='>=3.6',
)