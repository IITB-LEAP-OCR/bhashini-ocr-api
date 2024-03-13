# Layout Parser API

## Overview

Implementation of the Layout Parser API, specifically intergration of the Layout Detection code for various classes (Tables, Equations, Figures and Text) from Bhasini OCR API Repository. Implemented in docker. Processing code repository [here](https://github.com/iitb-research-code/docker-page-layout), use to build docker image.

## Changes Made
### layout_detection module
- Introduced layout_detection module, consolidating layout detection code for Tables, Equations, Figures, and Text, aiming to enhance code organization and maintainability in the Layout Parser API.

### routes.py
- Introduced `page/layout/table` as the primary endpoint for performing table detection.
- Introduced `page/layout/graphics/equation` as the primary endpoint for performing equation detection.
- Introduced `page/layout/graphics/photo` as the primary endpoint for performing figure detection.
- User inputs an images and a json response containing the bounding boxes for various classes is returned.

### helpers.py
- The `delete_files_in_directory` function is used to clear the contents of a directory before saving new files. 
- The `save_uploaded_images` function is implemented for saving uploaded images to a specified directory, replacing any existing files with the same names.

### models.py
- The code snippet defines a Pydantic model named LayoutDetection, which is intended to represent an uploaded file for layout detection. The purpose of this code is to create a structured way to handle uploaded files in FastAPI endpoints. 

In modules/page/__init__.py line 11 imported router from routes.py of the layout_detect.

In app.py line 38 imported router of page.

### Requirements

No need for external requirements as docker container is used for running

## Input and Example JSON Response

**Input:**
- An image file.

**Example JSON Response for Successful Table Detection:**
```json
{
    "message": "Table Detection Successful",
    "layout": {
        "tables": [
        [
            1172,
            2060,
            1512,
            2298
        ],
        [
            69,
            1945,
            95,
            1982
        ],
        [
            1477,
            2049,
            1516,
            2078
        ]
        // ... additional bounding boxes for tables
        ],
        "cells": [
        [
            58,
            3,
            808,
            63
        ]
        // ... additional bounding boxes for cells
        ]
    }
}
```

**Example JSON Response for Successful Equation Detection:**
```json
{
    "message": "Equation Detection Successful",
    "layout": {
        "equations": [
        [
            207,
            22,
            306,
            83
        ],
        [
            303,
            610,
            391,
            654
        ]

        // ... additional bounding boxes for equations
        ],
    }
}
```

**Example JSON Response for Successful Figure Detection:**
```json
{
    "message": "Figure Detection Successful",
    "layout": {
        "figures": [
        [
            52,
            106,
            122,
            139
        ]

        // ... additional bounding boxes for figures
        ],
    }
}
```