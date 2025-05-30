import os
import json
import argparse
import tempfile
import shutil
import cv2 # For image loading and some processing
from PIL import Image # For checking image type, sometimes used by tesseract

# Project-specific imports
from src.pdf_to_image import convert_pdf_to_images
from src.image_processor import to_grayscale, apply_binarization, apply_noise_reduction # deskew_image is optional
from src.ocr_extractor import extract_text_from_image
from src.data_structurer import structure_text_data

def main():
    parser = argparse.ArgumentParser(
        description="OCR and Data Extraction Pipeline for Lab Reports.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Shows default values in help
    )
    parser.add_argument("input_file", help="Path to the input PDF or image file.")
    parser.add_argument("output_json", help="Path to save the final JSON output.")

    # OCR parameters group
    ocr_group = parser.add_argument_group('OCR Parameters')
    ocr_group.add_argument("--lang", help="Language for OCR (e.g., 'eng', 'deu'). See Tesseract docs for available languages.")
    ocr_group.add_argument("--psm", type=int, help="Tesseract Page Segmentation Mode (0-13). See Tesseract docs.")
    ocr_group.add_argument("--oem", type=int, help="Tesseract OCR Engine Mode (0-3). See Tesseract docs.")

    # Preprocessing controls group
    preprocess_group = parser.add_argument_group('Preprocessing Parameters')
    preprocess_group.add_argument("--no-grayscale", action="store_true", help="Skip grayscale conversion.")
    preprocess_group.add_argument("--no-binarize", action="store_true", help="Skip binarization step.")
    preprocess_group.add_argument("--binarization-method", choices=['otsu', 'adaptive'],
                                  help="Binarization method if not skipped.")
    preprocess_group.add_argument("--no-noise-reduction", action="store_true", help="Skip noise reduction (Gaussian blur).")
    preprocess_group.add_argument("--blur-kernel-size", type=int, nargs=2, metavar=('HEIGHT', 'WIDTH'),
                                  help="Kernel size for Gaussian blur (positive odd integers, e.g., 5 5).")

    # Set default values for cleaner help messages
    parser.set_defaults(lang='eng', psm=3, oem=3,
                        binarization_method='otsu', blur_kernel_size=[5,5])

    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found at '{args.input_file}'", file=sys.stderr) # Use sys.stderr
        # Consider sys.exit(1) if main() is the entry point and not called by other Python code.
        # For this project, main() is the entry point.
        import sys
        sys.exit(1)


    input_file_lower = args.input_file.lower()
    is_pdf = input_file_lower.endswith(".pdf")
    # More robust image extension checking, though main.py relies on cv2.imread success later
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.webp']
    is_image = any(input_file_lower.endswith(ext) for ext in image_extensions)

    if not is_pdf and not is_image:
        print(f"Error: Unsupported file type for '{args.input_file}'. Must be a PDF or a common image format ({', '.join(image_extensions)}).", file=sys.stderr)
        import sys
        sys.exit(1)

    temp_dir_obj = None # Stores TemporaryDirectory object for PDF page images
    image_paths_to_process = []
    processed_image_temp_files = [] # To store paths of temp images created for OCR

    try:
        if is_pdf:
            temp_dir_obj = tempfile.TemporaryDirectory(prefix="ocr_pdf_pages_")
            print(f"Converting PDF '{args.input_file}' to images in '{temp_dir_obj.name}'...")
            # pdf_to_image.py saves images as page_1.png, page_2.png etc.
            # pdf_to_image.py saves images as page_1.png, page_2.png etc.
            convert_pdf_to_images(args.input_file, temp_dir_obj.name) # This function prints progress

            # List the converted images from the temporary directory
            temp_image_files = [os.path.join(temp_dir_obj.name, f) for f in os.listdir(temp_dir_obj.name)
                                if f.lower().endswith(image_extensions)]
            image_paths_to_process = sorted(temp_image_files) # Sort to maintain page order

            if not image_paths_to_process:
                print(f"Error: PDF conversion did not produce any processable images from '{args.input_file}'.", file=sys.stderr)
                # temp_dir_obj will be cleaned up in finally block
                import sys
                sys.exit(1)
            print(f"PDF successfully converted into {len(image_paths_to_process)} image(s).")
        elif is_image:
            image_paths_to_process.append(args.input_file)

        all_pages_structured_data = [] # To store structured data from each page/image

        # --- Main Image Processing Loop ---
        for i, image_path in enumerate(image_paths_to_process):
            page_num_str = f"Page {i+1}/{len(image_paths_to_process)}" if is_pdf and len(image_paths_to_process) > 1 else ""
            print(f"\nProcessing {page_num_str}image: '{os.path.basename(image_path)}'")

            # 1. Load image using OpenCV
            print(f"  Loading image: {image_path}")
            img_cv = cv2.imread(image_path)
            if img_cv is None:
                print(f"  Warning: Could not load image '{image_path}' using OpenCV. Skipping this image.", file=sys.stderr)
                continue
                continue # Skip to next image if this one failed to load

            processed_image = img_cv.copy() # Work on a copy

            # 2. Apply image preprocessing steps based on arguments
            print("  Applying preprocessing steps...")
            if not args.no_grayscale:
                print("    Converting to grayscale...")
                processed_image = to_grayscale(processed_image)
            # Ensure image is grayscale before binarization if binarization is active
            elif not args.no_binarize and len(processed_image.shape) == 3:
                print("    Warning: Binarization is enabled, but grayscale was skipped on a color image. Converting to grayscale first.")
                processed_image = to_grayscale(processed_image)

            if not args.no_noise_reduction:
                kernel = tuple(args.blur_kernel_size)
                # Validate kernel (must be positive and odd)
                if not (kernel[0] > 0 and kernel[0] % 2 == 1 and kernel[1] > 0 and kernel[1] % 2 == 1):
                    print(f"    Warning: Invalid kernel size {args.blur_kernel_size}. Must be positive odd integers. Using default (5,5).", file=sys.stderr)
                    kernel = (5, 5)
                print(f"    Applying noise reduction (Gaussian blur) with kernel {kernel}...")
                processed_image = apply_noise_reduction(processed_image, kernel_size=kernel)

            if not args.no_binarize:
                if len(processed_image.shape) == 3:
                     print("    Error: Image is still color before binarization. This indicates an issue in the grayscale step. Skipping binarization.", file=sys.stderr)
                else:
                    print(f"    Applying binarization using '{args.binarization_method}' method...")
                    processed_image = apply_binarization(processed_image, threshold_method=args.binarization_method)

            # Optional: Deskewing could be added here
            # print("  (Skipping deskewing - placeholder function)")
            # processed_image = deskew_image(processed_image)

            # 3. Save preprocessed image to a temporary file (required by Pytesseract)
            # Using a temporary file with a .png extension is generally safe.
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png", prefix="ocr_proc_") as temp_img_file_obj:
                cv2.imwrite(temp_img_file_obj.name, processed_image)
                temp_img_filepath = temp_img_file_obj.name
            processed_image_temp_files.append(temp_img_filepath) # Add to list for cleanup
            print(f"  Preprocessed image saved temporarily to '{temp_img_filepath}'")

            # 4. Extract text using Tesseract OCR
            print(f"  Extracting text (lang='{args.lang}', psm={args.psm}, oem={args.oem})...")
            try:
                raw_text = extract_text_from_image(temp_img_filepath, lang=args.lang, psm=args.psm, oem=args.oem)
                if raw_text == "TesseractNotFoundError": # Check for specific error string
                     print("Critical Error: Tesseract is not installed or not found in your PATH. Aborting.", file=sys.stderr)
                     # No further processing possible without Tesseract. Exit code handled in main try-except.
                     raise pytesseract.TesseractNotFoundError
                elif not raw_text.strip():
                    print(f"  Warning: No text extracted from '{os.path.basename(image_path)}'.")
            except pytesseract.TesseractNotFoundError: # Catch if raised directly by extract_text_from_image
                raise # Re-raise to be caught by the main try-except block for cleanup and exit
            except Exception as ocr_err:
                print(f"  Error during OCR for '{os.path.basename(image_path)}': {ocr_err}", file=sys.stderr)
                raw_text = "" # Ensure raw_text is empty on error

            # 5. Structure the extracted text
            print("  Structuring extracted text...")
            structured_data = structure_text_data(raw_text)
            if not structured_data and raw_text.strip():
                print(f"  Warning: Text was extracted from '{os.path.basename(image_path)}', but no key-value pairs were structured.")
                # Optionally, include raw_text if no structure found but text exists
                structured_data["unstructured_raw_text"] = raw_text

            all_pages_structured_data.append(structured_data)
        # --- End of Image Processing Loop ---

        # 6. Consolidate and Write Output JSON
        output_data_final = {}
        if not all_pages_structured_data:
            print("Warning: No data was structured from any page/image.", file=sys.stderr)
            output_data_final = {"info": "No structured data could be extracted from the document."}
        elif len(all_pages_structured_data) == 1 and not is_pdf : # Single image input, or single page PDF
             output_data_final = all_pages_structured_data[0]
        else: # PDF with multiple pages, or to be explicit for single page PDF results
            output_data_final = {"document_source": os.path.basename(args.input_file), "pages": all_pages_structured_data}

        print(f"\nWriting final structured data to '{args.output_json}'...")
        with open(args.output_json, 'w') as f_out:
            json.dump(output_data_final, f_out, indent=4)
        print("Processing complete.")

    except FileNotFoundError as e:
        print(f"Error: A required file was not found - {e}", file=sys.stderr)
        import sys; sys.exit(1)
    except pytesseract.TesseractNotFoundError:
        # This is now the central place to catch this error
        print("Error: Tesseract OCR is not installed or not found in your system PATH.", file=sys.stderr)
        print("Please install Tesseract and ensure it's accessible.", file=sys.stderr)
        import sys; sys.exit(2) # Specific exit code for Tesseract issues
    except Exception as e:
        print(f"An unexpected critical error occurred: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        import sys; sys.exit(1)
    finally:
        # 7. Clean up all temporary files and directories
        print("\nCleaning up temporary files...")
        for temp_file in processed_image_temp_files:
            try:
                os.remove(temp_file)
                # print(f"  Cleaned up temporary image: {temp_file}")
            except OSError as e:
                print(f"  Warning: Could not delete temporary file '{temp_file}': {e}", file=sys.stderr)

        if temp_dir_obj: # If TemporaryDirectory object was created
            try:
                temp_dir_obj.cleanup()
                print(f"  Cleaned up temporary directory for PDF images: {temp_dir_obj.name}")
            except Exception as e:
                print(f"  Warning: Could not delete temporary directory '{temp_dir_obj.name}': {e}", file=sys.stderr)
        print("Cleanup finished.")


if __name__ == "__main__":
    # This import is here to allow TesseractNotFoundError to be caught in main()
    import pytesseract
    # It's also good practice to ensure Tesseract is callable early, but main() handles it.
    # try:
    #     pytesseract.get_tesseract_version()
    # except pytesseract.TesseractNotFoundError as e:
    #     print(f"CRITICAL: Tesseract not found on startup. {e}. Please install Tesseract OCR.", file=sys.stderr)
    #     import sys
    #     sys.exit(2) # Exit early if Tesseract is missing
    main()
