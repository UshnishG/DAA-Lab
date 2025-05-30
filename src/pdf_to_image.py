import os
import sys
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_images(pdf_path, output_dir):
    """
    Converts a PDF file to a series of images and saves them in the output directory.

    Args:
        pdf_path (str): The path to the PDF file.
        output_dir (str): The directory where the output images will be saved.
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Note: For pdf2image to work effectively, Poppler utilities must be installed
        # and accessible in the system's PATH. On some systems (like Windows),
        # you might need to explicitly provide the 'poppler_path' to convert_from_path,
        # e.g., images = convert_from_path(pdf_path, poppler_path=r"C:\path\to\poppler-xxx\bin")
        images = convert_from_path(pdf_path)

        if not images:
            print(f"Warning: No images were converted from PDF: {pdf_path}")
            return # Return if no images were found

        for i, image in enumerate(images):
            image_filename = f"page_{i+1}.png"
            image_filepath = os.path.join(output_dir, image_filename)
            image.save(image_filepath, "PNG")
            print(f"Saved {image_filepath}")
    except Exception as e:
        print(f"Error converting PDF to images: {e}", file=sys.stderr) # Use stderr for errors
        # It might be good to raise the exception or handle it more gracefully
        # depending on whether this script is used as a module or standalone.
        # For now, printing the error is sufficient for its use in main.py.

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/pdf_to_image.py <pdf_path> <output_directory>", file=sys.stderr)
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    output_images_dir = sys.argv[2]

    if not os.path.exists(pdf_file_path):
        print(f"Error: PDF file not found at '{pdf_file_path}'", file=sys.stderr)
        sys.exit(1)

    print(f"Attempting to convert '{pdf_file_path}' to images in '{output_images_dir}'...")
    convert_pdf_to_images(pdf_file_path, output_images_dir)
    print("PDF to image conversion process finished.")
