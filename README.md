# Bhashini OCR API (version-0)

## Description

This is an API that combines the functionalities of Layout Parsing and OCR providing the following endpoints.

| End Point  | Technical Details |
| :---: | :---: |
| /page/ocr  | Tesseract  |
| /page/layout/table |  Table Detection FRCNN Model  |
| /page/layout/text/word | TEXTRON |
| /page/layout/text/word/attr/style |  Font name and style  |
| /word/ocr  | Robust Hindi Model |
| /word/attr/script |  Script Detection  |
| /apps/page |  Layout Preserving OCR  |

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
5. To access the swagger UI redirect to http://0.0.0.0:8058/api/v0/docs