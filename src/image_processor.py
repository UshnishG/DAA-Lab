import cv2
import numpy as np

def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Converts an image to grayscale."""
    if len(image.shape) == 3 and image.shape[2] == 3: # Check if it's a color image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2: # Already grayscale
        return image
    else:
        raise ValueError("Unsupported image format for grayscale conversion. Expected 2D or 3D BGR image.")

def apply_binarization(image: np.ndarray, threshold_method: str = 'otsu') -> np.ndarray:
    """
    Converts a grayscale image to binary (black and white).

    Args:
        image (np.ndarray): Input grayscale image.
        threshold_method (str): 'otsu' or 'adaptive' or a fixed integer threshold value.
                                If 'adaptive', uses adaptive Gaussian thresholding.
                                If an integer, it's used as the fixed threshold.

    Returns:
        np.ndarray: Binary image.
    """
    if len(image.shape) == 3:
        # This case should ideally be handled by converting to grayscale first.
        # If a user calls this directly with a color image, it's an issue.
        raise ValueError("Binarization requires a grayscale image. Convert the image to grayscale first.")
    elif len(image.shape) != 2:
        raise ValueError("Binarization requires a 2D grayscale image.")

    if threshold_method == 'otsu':
        thresh_val, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif threshold_method == 'adaptive':
        binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                             cv2.THRESH_BINARY, 11, 2)
    elif isinstance(threshold_method, int):
        if not (0 <= threshold_method <= 255):
            raise ValueError("Fixed threshold must be between 0 and 255.")
        thresh_val, binary_image = cv2.threshold(image, threshold_method, 255, cv2.THRESH_BINARY)
    else:
        raise ValueError(f"Unsupported threshold method: {threshold_method}. Choose 'otsu', 'adaptive', or an integer.")
    return binary_image

def apply_noise_reduction(image: np.ndarray, kernel_size=(5,5)) -> np.ndarray:
    """
    Applies Gaussian blur to reduce noise.

    Args:
        image (np.ndarray): Input image.
        kernel_size (tuple): Kernel size for Gaussian blur. Must be odd positive integers.

    Returns:
        np.ndarray: Image with noise reduction applied.
    """
    if not (isinstance(kernel_size, tuple) and len(kernel_size) == 2 and
            kernel_size[0] > 0 and kernel_size[0] % 2 == 1 and
            kernel_size[1] > 0 and kernel_size[1] % 2 == 1):
        raise ValueError("Kernel size must be a tuple of two positive odd integers (e.g., (5,5)).")
    return cv2.GaussianBlur(image, kernel_size, 0)

def deskew_image(image: np.ndarray) -> np.ndarray:
    """
    Placeholder for image deskewing.
    Currently returns the image as is.

    A common approach involves:
    1. Convert to grayscale if not already.
    2. Binarize the image.
    3. Find contours (e.g., using cv2.findContours).
    4. For the largest contour (or relevant text block contour):
        a. Get the minimum area rectangle (cv2.minAreaRect).
        b. Get the angle from this rectangle.
        c. If the angle is significant, create a rotation matrix (cv2.getRotationMatrix2D)
           and apply affine transformation (cv2.warpAffine).
    """
    print("Placeholder: deskew_image() called, returning original image.")
    # Future implementation:
    # gray = to_grayscale(image) if len(image.shape) > 2 or image.shape[2] == 3 else image
    # binary = apply_binarization(gray, threshold_method='otsu')
    # # ... contour detection and rotation logic ...
    return image

if __name__ == '__main__':
    # This part is for basic testing if you run the script directly.
    # It's not a formal CLI but can be useful for development.
    # Ensure cv2 is available if running this block.
    print("image_processor.py loaded. Contains image processing functions.")
    print("This module is intended to be imported, not run directly for OCR tasks.")
    print("The following test block requires OpenCV to be installed to run without errors.")

    # Example of creating a dummy image and testing functions (requires OpenCV)
    # Create a sample image (e.g., 100x100, 3 channels, white)
    # sample_color_image = np.full((100, 100, 3), 255, dtype=np.uint8)
    # cv2.putText(sample_color_image, "Test", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    # if cv2 is not None :
    #     try:
    #         print("Testing with a sample image...")
    #         # Create a sample color image
    #         test_img_color = np.zeros((100, 200, 3), dtype=np.uint8)
    #         cv2.putText(test_img_color, 'Hello', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)

    #         print(f"Original image shape: {test_img_color.shape}")

    #         gray_img = to_grayscale(test_img_color)
    #         print(f"Grayscale image shape: {gray_img.shape}")

    #         blurred_img = apply_noise_reduction(gray_img) # Using default kernel
    #         print(f"Blurred image shape: {blurred_img.shape}")

    #         binary_img_otsu = apply_binarization(blurred_img, threshold_method='otsu')
    #         print(f"Otsu binary image shape: {binary_img_otsu.shape}")

    #         # Create a slightly skewed image for deskew testing (manual rotation)
    #         # This is a very basic skew for demonstration
    #         # center = (gray_img.shape[1]//2, gray_img.shape[0]//2)
    #         # angle = 5
    #         # scale = 1.0
    #         # rot_mat = cv2.getRotationMatrix2D(center, angle, scale)
    #         # skewed_gray_img = cv2.warpAffine(gray_img, rot_mat, (gray_img.shape[1], gray_img.shape[0]), flags=cv2.INTER_LINEAR, borderValue=(255,255,255))

    #         deskewed_img = deskew_image(gray_img) # Pass grayscale to deskew
    #         print(f"Deskewed image shape (placeholder): {deskewed_img.shape}")

    #         print("Basic function tests completed (visually inspect if images were displayed/saved).")

    #     except ImportError:
    #         print("cv2 (OpenCV) is not installed. Cannot run visual tests for image_processor.py.")
    #     except Exception as e:
    #         print(f"An error occurred during self-testing: {e}")
    # else:
    #     print("cv2 (OpenCV) is not available. Cannot run self-tests in image_processor.py")
