# Complex OCR Application for Lab Reports

## Overview

This application processes PDF and image-based lab reports to extract structured information using Optical Character Recognition (OCR). It aims to convert the textual content of these reports into a machine-readable JSON format, making it easier to access and analyze key data points.

## Features

*   **Input Flexibility:** Accepts both PDF files and common image formats (PNG, JPG, TIFF, etc.) as input.
*   **PDF Processing:** Converts multi-page PDFs into individual images for OCR.
*   **Image Preprocessing:** Includes steps for:
    *   Grayscale conversion
    *   Noise reduction (Gaussian Blur)
    *   Binarization (Otsu's or adaptive thresholding)
    *   (Placeholder for future deskewing)
*   **OCR Engine:** Utilizes Tesseract OCR for text extraction. Users can specify language, Page Segmentation Mode (PSM), and OCR Engine Mode (OEM).
*   **Basic Data Structuring:** Employs regular expressions to identify and extract common lab report fields (e.g., Patient Name, Report Date, Test ID, Results).
*   **JSON Output:** Saves the extracted and structured data in a JSON file. For multi-page documents, data from each page is included.
*   **Command-Line Interface:** Allows users to run the application and control its parameters via `main.py`.
*   **Test Script:** Includes a shell script (`test_application.sh`) to demonstrate basic functionality using sample data.

## Project Structure

```
.
├── README.md               # This documentation file
├── requirements.txt        # Python dependencies
├── main.py                 # Main application script to run the OCR pipeline
├── test_application.sh     # Shell script to test the application with sample data
├── data/                   # Directory for sample input documents
│   ├── sample_lab_report.txt # Original text for sample documents
│   ├── sample_lab_report.pdf # Sample PDF generated from the text
│   └── sample_lab_report.png # Sample image generated from the text
├── src/                    # Source code for different modules
│   ├── pdf_to_image.py     # Module for converting PDF to images
│   ├── image_processor.py  # Module for image preprocessing functions
│   ├── ocr_extractor.py    # Module for core Tesseract OCR text extraction
│   └── data_structurer.py  # Module for structuring extracted text into key-value pairs
└── output/                 # Directory for saving output JSON files (created by scripts)
    ├── pdf_output.json     # Sample output from PDF processing via test script
    └── image_output.json   # Sample output from image processing via test script
```

## Setup and Installation

1.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install Tesseract OCR:**
    Tesseract OCR is a system dependency. You need to install it separately.
    *   **Linux (Ubuntu/Debian):**
        ```bash
        sudo apt-get update
        sudo apt-get install tesseract-ocr
        sudo apt-get install libtesseract-dev # For development headers if needed
        # Also install language packs, e.g., for English:
        sudo apt-get install tesseract-ocr-eng
        ```
    *   **macOS (using Homebrew):**
        ```bash
        brew install tesseract
        # Install language packs if needed, e.g., brew install tesseract-lang
        ```
    *   **Windows:** Download the installer from the official Tesseract GitHub page (e.g., from [UB Mannheim Tesseract Builds](https://github.com/UB-Mannheim/tesseract/wiki)). Ensure you add Tesseract to your system's PATH environment variable during or after installation.

    For detailed instructions, please search online: "install tesseract ocr [your_os]".

3.  **Install Python Dependencies:**
    Navigate to the project root directory (where `requirements.txt` is located) and run:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `pytesseract`, `Pillow`, `opencv-python`, `pdf2image`, and `numpy`.

## Running the Application

The main script for processing documents is `main.py`.

**Example Command:**
```bash
python main.py data/sample_lab_report.pdf output/report_data.json
```

**Command-Line Arguments for `main.py`:**

*   `input_file`: (Required) Path to the input PDF or image file.
*   `output_json`: (Required) Path to save the final JSON output.
*   `--lang <language>`: Language for OCR (default: `eng`). Example: `--lang deu` for German.
*   `--psm <mode>`: Tesseract Page Segmentation Mode (0-13, default: `3`).
*   `--oem <mode>`: Tesseract OCR Engine Mode (0-3, default: `3`).
*   `--no-grayscale`: Skip grayscale conversion.
*   `--no-binarize`: Skip binarization.
*   `--binarization-method <method>`: Choose 'otsu' or 'adaptive' (default: `otsu`).
*   `--no-noise-reduction`: Skip noise reduction.
*   `--blur-kernel-size <height width>`: Kernel size for Gaussian blur (default: `5 5`).

## Running the Test Script

A test script `test_application.sh` is provided to quickly verify the basic pipeline.

**How to Run:**
```bash
bash test_application.sh
```
Or, if you've made it executable:
```bash
./test_application.sh
```

**What it Does:**
*   Ensures the `output/` directory exists.
*   Processes `data/sample_lab_report.pdf` and saves the result to `output/pdf_output.json`.
*   Processes `data/sample_lab_report.png` and saves the result to `output/image_output.json`.
*   Prints success or error messages based on the exit codes of the processing steps.
*   Prompts you to manually inspect the output JSON files.

## Potential Future Improvements/Refinements

This application provides a foundational OCR pipeline. Many enhancements can be made:

*   **Advanced Layout Analysis:** Implement or integrate tools (e.g., LayoutLM, Detectron2, or custom computer vision models) to better understand document structure, identify text blocks, columns, and tables.
*   **Robust Table Extraction:** Develop specific logic for accurately extracting data from tabular structures.
*   **Improved Accuracy for Complex Scans:**
    *   More sophisticated image preprocessing techniques (e.g., adaptive thresholding based on local properties, advanced deskewing, perspective correction).
    *   Explore cloud-based OCR services (Google Cloud Vision AI, AWS Textract) for potentially higher accuracy on challenging documents.
*   **Configuration File:** Move regex patterns, default OCR settings, and other parameters to an external configuration file (e.g., YAML or JSON) for easier customization.
*   **Comprehensive Error Handling & Logging:** Implement more granular error handling and detailed logging throughout the pipeline for easier debugging and monitoring.
*   **Graphical User Interface (GUI):** Develop a GUI (e.g., using PyQt, Tkinter, or a web framework like Flask/Django) for easier use by non-technical users.
*   **LLM Integration:** Integrate Large Language Models (LLMs) for:
    *   More intelligent data structuring from raw OCR text.
    *   Natural Language Understanding (NLU) on extracted data.
    *   Summarization or querying of report content.
*   **Comprehensive Testing:** Expand unit tests for each module and add integration tests for the entire pipeline.
*   **Batch Processing:** Allow processing of multiple files from a directory.
*   **Output Formats:** Support other output formats besides JSON (e.g., CSV, XML).

---
This README provides a starting point. Feel free to expand it as the project evolves.
```
