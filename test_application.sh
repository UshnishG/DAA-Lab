#!/bin/bash

# Ensure the output directory exists
mkdir -p output

# Define input files and output JSON paths
PDF_INPUT="data/sample_lab_report.pdf"
IMAGE_INPUT="data/sample_lab_report.png"
PDF_OUTPUT="output/pdf_output.json"
IMAGE_OUTPUT="output/image_output.json"

# Variable to track overall success
OVERALL_SUCCESS=true

echo "Starting application test..."

# Test with PDF input
echo "-----------------------------------------------------"
echo "Running main.py with PDF input: $PDF_INPUT"
python main.py "$PDF_INPUT" "$PDF_OUTPUT" --lang eng
PDF_EXIT_CODE=$?

if [ $PDF_EXIT_CODE -eq 0 ]; then
    echo "PDF processing completed successfully (Exit Code: $PDF_EXIT_CODE)."
    if [ -s "$PDF_OUTPUT" ]; then
        echo "Output JSON for PDF is not empty: $PDF_OUTPUT"
    else
        echo "Warning: Output JSON for PDF is EMPTY: $PDF_OUTPUT"
        # OVERALL_SUCCESS=false # Depending on strictness, an empty JSON might be a failure
    fi
else
    echo "Error: PDF processing failed (Exit Code: $PDF_EXIT_CODE)."
    OVERALL_SUCCESS=false
fi

# Test with Image input
echo "-----------------------------------------------------"
echo "Running main.py with Image input: $IMAGE_INPUT"
python main.py "$IMAGE_INPUT" "$IMAGE_OUTPUT" --lang eng
IMAGE_EXIT_CODE=$?

if [ $IMAGE_EXIT_CODE -eq 0 ]; then
    echo "Image processing completed successfully (Exit Code: $IMAGE_EXIT_CODE)."
    if [ -s "$IMAGE_OUTPUT" ]; then
        echo "Output JSON for Image is not empty: $IMAGE_OUTPUT"
    else
        echo "Warning: Output JSON for Image is EMPTY: $IMAGE_OUTPUT"
        # OVERALL_SUCCESS=false # Depending on strictness
    fi
else
    echo "Error: Image processing failed (Exit Code: $IMAGE_EXIT_CODE)."
    OVERALL_SUCCESS=false
fi
echo "-----------------------------------------------------"

if [ "$OVERALL_SUCCESS" = true ]; then
    echo "All tests completed. Output files are saved in the 'output' directory."
    echo "Please manually inspect:"
    echo "- $PDF_OUTPUT"
    echo "- $IMAGE_OUTPUT"
    echo "to verify the content of the extracted data."
    exit 0
else
    echo "Some tests failed. Please review the logs above."
    exit 1
fi
