"""
Utility functions for the Image to Cartoon Converter
"""

import os
import uuid
from typing import Tuple
import cv2
import numpy as np
from PIL import Image
import io


def allowed_file(filename: str, allowed_extensions: set = None) -> bool:
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file
        allowed_extensions: Set of allowed extensions
        
    Returns:
        True if extension is allowed
    """
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename using UUID
    
    Args:
        original_filename: Original filename
        
    Returns:
        Unique filename with same extension
    """
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{extension}"


def ensure_dir_exists(directory: str) -> None:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory: Directory path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """
    Read image from bytes
    
    Args:
        image_bytes: Image data as bytes
        
    Returns:
        Image as numpy array (BGR format for OpenCV)
    """
    # Convert bytes to PIL Image
    pil_image = Image.open(io.BytesIO(image_bytes))
    
    # Convert RGBA to RGB if necessary
    if pil_image.mode == 'RGBA':
        pil_image = pil_image.convert('RGB')
    
    # Convert to numpy array
    image_array = np.array(pil_image)
    
    # Convert RGB to BGR for OpenCV
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    return image_bgr


def image_to_bytes(image: np.ndarray, format: str = 'JPEG') -> bytes:
    """
    Convert numpy image array to bytes
    
    Args:
        image: Image as numpy array (BGR format)
        format: Output format (JPEG, PNG, etc.)
        
    Returns:
        Image as bytes
    """
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert to PIL Image
    pil_image = Image.fromarray(image_rgb)
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format=format, quality=95)
    img_byte_arr.seek(0)
    
    return img_byte_arr.getvalue()


def resize_image(image: np.ndarray, max_size: Tuple[int, int] = (1920, 1080)) -> np.ndarray:
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: Input image
        max_size: Maximum (width, height)
        
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    max_width, max_height = max_size
    
    # Calculate scaling factor
    scale = min(max_width / width, max_height / height, 1.0)
    
    if scale < 1.0:
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized = cv2.resize(image, (new_width, new_height), 
                           interpolation=cv2.INTER_AREA)
        return resized
    
    return image


def cleanup_old_files(directory: str, max_age_hours: int = 24) -> int:
    """
    Clean up old files from a directory
    
    Args:
        directory: Directory to clean
        max_age_hours: Maximum age of files to keep (in hours)
        
    Returns:
        Number of files deleted
    """
    import time
    
    if not os.path.exists(directory):
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    deleted_count = 0
    
    for filename in os.listdir(directory):
        if filename == '.gitkeep':
            continue
            
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            file_age = current_time - os.path.getmtime(filepath)
            
            if file_age > max_age_seconds:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {filepath}: {e}")
    
    return deleted_count


def validate_image(image_bytes: bytes, max_size_mb: int = 10) -> Tuple[bool, str]:
    """
    Validate uploaded image
    
    Args:
        image_bytes: Image data as bytes
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > max_size_mb:
        return False, f"File size ({size_mb:.2f}MB) exceeds maximum ({max_size_mb}MB)"
    
    # Try to open image
    try:
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Check image dimensions
        width, height = pil_image.size
        if width < 50 or height < 50:
            return False, "Image dimensions too small (minimum 50x50)"
        
        if width > 10000 or height > 10000:
            return False, "Image dimensions too large (maximum 10000x10000)"
        
        # Verify it's a valid image format
        pil_image.verify()
        
        return True, ""
        
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def create_thumbnail(image: np.ndarray, size: Tuple[int, int] = (300, 300)) -> np.ndarray:
    """
    Create a thumbnail of the image
    
    Args:
        image: Input image
        size: Thumbnail size (width, height)
        
    Returns:
        Thumbnail image
    """
    height, width = image.shape[:2]
    thumb_width, thumb_height = size
    
    # Calculate scaling to fit within thumbnail size
    scale = min(thumb_width / width, thumb_height / height)
    
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    thumbnail = cv2.resize(image, (new_width, new_height), 
                          interpolation=cv2.INTER_AREA)
    
    return thumbnail


def apply_watermark(image: np.ndarray, text: str = "CartoonConverter") -> np.ndarray:
    """
    Apply a subtle watermark to the image
    
    Args:
        image: Input image
        text: Watermark text
        
    Returns:
        Image with watermark
    """
    result = image.copy()
    height, width = result.shape[:2]
    
    # Position at bottom right
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    color = (255, 255, 255)  # White
    
    # Get text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Position
    x = width - text_width - 10
    y = height - 10
    
    # Add semi-transparent background
    overlay = result.copy()
    cv2.rectangle(overlay, (x - 5, y - text_height - 5), 
                 (x + text_width + 5, y + 5), (0, 0, 0), -1)
    result = cv2.addWeighted(result, 0.7, overlay, 0.3, 0)
    
    # Add text
    cv2.putText(result, text, (x, y), font, font_scale, color, thickness, cv2.LINE_AA)
    
    return result


# Example usage
if __name__ == "__main__":
    print("🔧 Utility Functions for Image to Cartoon Converter")
    print("\nAvailable functions:")
    print("- allowed_file: Validate file extensions")
    print("- generate_unique_filename: Create unique filenames")
    print("- read_image_from_bytes: Convert bytes to image array")
    print("- image_to_bytes: Convert image array to bytes")
    print("- resize_image: Resize while maintaining aspect ratio")
    print("- validate_image: Validate uploaded images")
    print("- cleanup_old_files: Remove old temporary files")
    print("- create_thumbnail: Generate thumbnails")
    print("- apply_watermark: Add watermark to images")
