# Bhashini OCR API (version-1)

## Description

This is an API that combines the functionalities of Layout Parsing and OCR providing the following endpoints.

| End Point  | Technical Details |
| :---: | :---: |
| /page/layout/table |  Table Detection  |
| /page/layout/text/word | TEXTRON (Text Detection) |
| /page/layout/text/word/attr/style |  Text Attribute Detection  |
| /word/attr/script |  Script Detection  |
| /page/ocr  | OCR using Tesseract |
| /word/ocr  | Robust Hindi OCR |
| /apps/page |  Layout Preserving OCR  |

## Resources
1. [API Documentation](https://docs.google.com/document/d/1n6hQ8GsPeaaBxNYfzmjgeI_tuNJTxnx9c9cVD-RD3Uw/edit?usp=sharing)
2. [Testing Report](https://docs.google.com/document/d/1wx_iKTE1Knd6Os95OrVe0fog2Nma8TZq7kSvstC9moA/edit?usp=sharing)
   

## Getting Started
1. Clone the repository to local system
   ```
   git clone -b version-0 https://github.com/IITB-LEAP-OCR/bhashini-ocr-api.git
   ```
2. Create a python3 virtualenv and activate it
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the required python packages
   ```
    pip3 install -r requirements.txt
   ```
4. Simply run the main.py file
   ```
    python3 main.py
   ```
5. To access the swagger UI redirect to http://0.0.0.0:8058/api/v1/docs
