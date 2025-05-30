import pytesseract
from PIL import Image
import argparse
import os
import sys # Ensure sys is imported for sys.exit and sys.stderr

def extract_text_from_image(image_path: str, lang: str = 'eng', psm: int = 3, oem: int = 3) -> str:
    """
    Extracts text from an image using Tesseract OCR.

    Args:
        image_path (str): Path to the input image file.
        lang (str): Language for OCR (e.g., 'eng', 'fra').
        psm (int): Tesseract Page Segmentation Mode (0-13).
        oem (int): Tesseract OCR Engine Mode (0-3).

    Returns:
        str: The extracted raw text.
    """
    if not os.path.exists(image_path):
        # This exception is fine for the function's contract
        raise FileNotFoundError(f"Image file not found at '{image_path}'")

    try:
        image = Image.open(image_path)
        custom_config = f'--psm {psm} --oem {oem}'
        text = pytesseract.image_to_string(image, lang=lang, config=custom_config)
        return text
    except pytesseract.TesseractNotFoundError:
        # Specific error for Tesseract not being installed/found
        print("Error: Tesseract is not installed or not found in your PATH.", file=sys.stderr)
        # Re-raise or exit, depending on how this function is meant to be used by a larger app
        # For CLI usage, exiting might be desired. For library usage, re-raising is better.
        # Let's make it print and return empty string for now, CLI can handle exit.
        return "TesseractNotFoundError" # Special string to indicate this specific error
    except Exception as e:
        print(f"Error during OCR extraction: {e}", file=sys.stderr)
        return "" # Return empty string on other errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract text from an image using Tesseract OCR.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Shows default values in help
    )
    parser.add_argument("image_path", help="Path to the input image file.")
    parser.add_argument("--lang", help="Language for OCR (e.g., 'eng', 'deu').")
    parser.add_argument("--psm", type=int,
                        help="Tesseract Page Segmentation Mode (0-13). See Tesseract docs for details.")
    parser.add_argument("--oem", type=int,
                        help="Tesseract OCR Engine Mode (0-3). See Tesseract docs for details.")

    # Set defaults here instead of in add_argument to make help message cleaner for those with defaults
    parser.set_defaults(lang='eng', psm=3, oem=3)

    args = parser.parse_args()

    if not (0 <= args.psm <= 13):
        print(f"Error: Invalid PSM value {args.psm}. Must be between 0 and 13.", file=sys.stderr)
        sys.exit(1)

    if not (0 <= args.oem <= 3):
        print(f"Error: Invalid OEM value {args.oem}. Must be between 0 and 3.", file=sys.stderr)
        sys.exit(1)

    try:
        # Check file existence here for the CLI part for a clearer error message before calling the function
        if not os.path.exists(args.image_path):
            print(f"Error: Image file not found at '{args.image_path}'", file=sys.stderr)
            sys.exit(1)

        extracted_text = extract_text_from_image(args.image_path, args.lang, args.psm, args.oem)

        if extracted_text == "TesseractNotFoundError":
            # Specific handling for Tesseract not found error from the function
            sys.exit(2) # Use a different exit code for this specific error

        print("Extracted Text:")
        print("-------------------")
        print(extracted_text)
        print("-------------------")

    except FileNotFoundError as e: # Should be caught by the os.path.exists check above now
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e: # Catch any other unexpected errors
        print(f"An unexpected error occurred in CLI: {e}", file=sys.stderr)
        sys.exit(1)
