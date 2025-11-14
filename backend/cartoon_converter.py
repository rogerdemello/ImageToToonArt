"""
Image Processing-based Cartoon Converter using OpenCV
Implements classic cartoon effect with edge detection and color quantization
"""

import cv2
import numpy as np
from typing import Tuple


class CartoonConverter:
    """Convert images to cartoon style using image processing techniques"""
    
    def __init__(self):
        self.default_params = {
            'bilateral_d': 9,
            'bilateral_sigma_color': 300,
            'bilateral_sigma_space': 300,
            'median_blur_kernel': 7,
            'edge_block_size': 9,
            'edge_c': 2,
            'color_clusters': 12  # Increased for better color detail
        }
    
    def convert(self, image: np.ndarray, style: str = 'classic') -> np.ndarray:
        """
        Convert image to cartoon style
        
        Args:
            image: Input image as numpy array (BGR format)
            style: Cartoon style ('classic', 'smooth', 'edge_heavy', 'ultra')
            
        Returns:
            Cartoonized image as numpy array
        """
        if style == 'classic':
            return self._classic_cartoon(image)
        elif style == 'smooth':
            return self._smooth_cartoon(image)
        elif style == 'edge_heavy':
            return self._edge_heavy_cartoon(image)
        elif style == 'ultra':
            return self._ultra_quality_cartoon(image)
        else:
            return self._classic_cartoon(image)
    
    def _classic_cartoon(self, image: np.ndarray) -> np.ndarray:
        """
        ENHANCED Classic cartoon effect with balanced edges and colors
        
        Process:
        1. Apply bilateral filter for edge-preserving smoothing (multiple passes)
        2. Detect edges using adaptive thresholding
        3. Quantize colors using K-means clustering
        4. Combine edges with quantized colors
        5. Apply contrast enhancement
        """
        # Step 1: Smooth the image while preserving edges (double pass for better quality)
        smooth = cv2.bilateralFilter(
            image,
            d=self.default_params['bilateral_d'],
            sigmaColor=self.default_params['bilateral_sigma_color'],
            sigmaSpace=self.default_params['bilateral_sigma_space']
        )
        smooth = cv2.bilateralFilter(
            smooth,
            d=self.default_params['bilateral_d'],
            sigmaColor=self.default_params['bilateral_sigma_color'],
            sigmaSpace=self.default_params['bilateral_sigma_space']
        )
        
        # Step 2: Detect edges with better quality
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, self.default_params['median_blur_kernel'])
        edges = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=self.default_params['edge_block_size'],
            C=self.default_params['edge_c']
        )
        
        # Step 3: Quantize colors (reduce color palette)
        quantized = self._quantize_colors(
            smooth,
            k=self.default_params['color_clusters']
        )
        
        # Step 4: Enhance saturation for vibrant cartoon colors
        quantized_hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
        quantized_hsv[:, :, 1] = np.clip(quantized_hsv[:, :, 1] * 1.2, 0, 255)  # Boost saturation
        quantized = cv2.cvtColor(quantized_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 5: Combine edges with quantized colors
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(quantized, edges_colored)
        
        # Step 6: Apply subtle sharpening for crisp results
        kernel = np.array([[0, -1, 0],
                          [-1, 5, -1],
                          [0, -1, 0]])
        cartoon = cv2.filter2D(cartoon, -1, kernel)
        
        return cartoon
    
    def _smooth_cartoon(self, image: np.ndarray) -> np.ndarray:
        """
        Smoother cartoon effect with less prominent edges
        """
        # Apply stronger bilateral filtering
        smooth = cv2.bilateralFilter(image, d=15, sigmaColor=80, sigmaSpace=80)
        
        # Apply additional smoothing
        smooth = cv2.bilateralFilter(smooth, d=9, sigmaColor=300, sigmaSpace=300)
        
        # Detect edges with less sensitivity
        gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=5
        )
        
        # Quantize colors
        quantized = self._quantize_colors(smooth, k=6)
        
        # Combine
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(quantized, edges_colored)
        
        return cartoon
    
    def _edge_heavy_cartoon(self, image: np.ndarray) -> np.ndarray:
        """
        ENHANCED Cartoon effect with prominent, bold edges
        """
        # Smooth the image
        smooth = cv2.bilateralFilter(image, d=9, sigmaColor=250, sigmaSpace=250)
        
        # Detect edges with higher sensitivity
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use multiple edge detection methods and combine
        # Method 1: Canny edges
        edges_canny = cv2.Canny(gray, 50, 150)
        
        # Method 2: Adaptive threshold
        gray_blur = cv2.medianBlur(gray, 5)
        edges_adaptive = cv2.adaptiveThreshold(
            gray_blur, 255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            blockSize=9,
            C=2
        )
        
        # Combine edge detection methods
        edges = cv2.bitwise_or(cv2.bitwise_not(edges_canny), edges_adaptive)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((2, 2), np.uint8))
        
        # Quantize colors with more clusters for detail
        quantized = self._quantize_colors(smooth, k=14)
        
        # Boost saturation and contrast
        quantized_hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
        quantized_hsv[:, :, 1] = np.clip(quantized_hsv[:, :, 1] * 1.3, 0, 255)  # Saturation
        quantized_hsv[:, :, 2] = np.clip(quantized_hsv[:, :, 2] * 1.1, 0, 255)  # Brightness
        quantized = cv2.cvtColor(quantized_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Combine
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(quantized, edges_colored)
        
        return cartoon
    
    def _ultra_quality_cartoon(self, image: np.ndarray) -> np.ndarray:
        """
        ULTRA QUALITY - Best possible cartoon effect
        Uses advanced techniques for professional results
        """
        # Step 1: Denoise with non-local means (slower but best quality)
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        
        # Step 2: Multiple bilateral filter passes for ultra-smooth colors
        smooth = denoised
        for _ in range(3):
            smooth = cv2.bilateralFilter(smooth, d=9, sigmaColor=75, sigmaSpace=75)
        
        # Step 3: Advanced edge detection with multiple methods
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Sobel edges for gradient-based detection
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = np.sqrt(sobelx**2 + sobely**2)
        sobel = np.uint8(255 * sobel / np.max(sobel))
        _, edges_sobel = cv2.threshold(sobel, 50, 255, cv2.THRESH_BINARY_INV)
        
        # Adaptive threshold for local edges
        gray_blur = cv2.medianBlur(gray, 7)
        edges_adaptive = cv2.adaptiveThreshold(
            gray_blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,
            C=2
        )
        
        # Canny for sharp edges
        edges_canny = cv2.Canny(gray, 30, 100)
        edges_canny = cv2.dilate(edges_canny, np.ones((2, 2), np.uint8), iterations=1)
        edges_canny = cv2.bitwise_not(edges_canny)
        
        # Combine all edge detection methods
        edges = cv2.bitwise_and(edges_sobel, edges_adaptive)
        edges = cv2.bitwise_and(edges, edges_canny)
        
        # Morphological operations for cleaner edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Step 4: High-quality color quantization with more colors
        quantized = self._quantize_colors(smooth, k=16)
        
        # Step 5: Enhance colors for vibrant cartoon look
        lab = cv2.cvtColor(quantized, cv2.COLOR_BGR2LAB).astype(np.float32)
        lab[:, :, 0] = np.clip(lab[:, :, 0] * 1.05, 0, 255)  # Slight brightness boost
        quantized = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
        
        hsv = cv2.cvtColor(quantized, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.4, 0, 255)  # Strong saturation boost
        quantized = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        # Step 6: Combine edges with quantized colors
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        cartoon = cv2.bitwise_and(quantized, edges_colored)
        
        # Step 7: Apply advanced sharpening
        gaussian = cv2.GaussianBlur(cartoon, (0, 0), 2.0)
        cartoon = cv2.addWeighted(cartoon, 1.5, gaussian, -0.5, 0)
        
        # Step 8: Final contrast enhancement with CLAHE
        lab = cv2.cvtColor(cartoon, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        cartoon = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return cartoon
    
    def _quantize_colors(self, image: np.ndarray, k: int = 8) -> np.ndarray:
        """
        Reduce the number of colors in the image using K-means clustering
        
        Args:
            image: Input image
            k: Number of color clusters
            
        Returns:
            Image with quantized colors
        """
        # Reshape image to be a list of pixels
        pixels = image.reshape((-1, 3))
        pixels = np.float32(pixels)
        
        # Define criteria and apply K-means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        _, labels, centers = cv2.kmeans(
            pixels,
            k,
            None,
            criteria,
            10,
            cv2.KMEANS_RANDOM_CENTERS
        )
        
        # Convert back to 8-bit values
        centers = np.uint8(centers)
        
        # Map each pixel to its center
        quantized = centers[labels.flatten()]
        
        # Reshape back to original image shape
        quantized = quantized.reshape(image.shape)
        
        return quantized
    
    def stylize_pencil_sketch(self, image: np.ndarray, 
                             color: bool = False) -> np.ndarray:
        """
        Create a pencil sketch effect
        
        Args:
            image: Input image
            color: If True, creates colored pencil sketch
            
        Returns:
            Pencil sketch image
        """
        if color:
            sketch_gray, sketch_color = cv2.pencilSketch(
                image,
                sigma_s=60,
                sigma_r=0.07,
                shade_factor=0.05
            )
            return sketch_color
        else:
            sketch_gray, _ = cv2.pencilSketch(
                image,
                sigma_s=60,
                sigma_r=0.07,
                shade_factor=0.05
            )
            return sketch_gray
    
    def stylize_oil_painting(self, image: np.ndarray) -> np.ndarray:
        """
        Create an oil painting effect
        
        Args:
            image: Input image
            
        Returns:
            Oil painting styled image
        """
        # Apply stylization
        result = cv2.stylization(image, sigma_s=60, sigma_r=0.6)
        return result
    
    def get_available_styles(self) -> list:
        """Return list of available cartoon styles"""
        return ['classic', 'smooth', 'edge_heavy', 'ultra', 'pencil_sketch', 
                'pencil_sketch_color', 'oil_painting']


# Example usage and testing
if __name__ == "__main__":
    import os
    
    converter = CartoonConverter()
    
    # Test with a sample image (you'll need to provide your own)
    test_image_path = "../examples/sample.jpg"
    
    if os.path.exists(test_image_path):
        # Read image
        img = cv2.imread(test_image_path)
        
        # Convert to different styles
        classic = converter.convert(img, 'classic')
        smooth = converter.convert(img, 'smooth')
        edge_heavy = converter.convert(img, 'edge_heavy')
        pencil = converter.stylize_pencil_sketch(img, color=False)
        oil = converter.stylize_oil_painting(img)
        
        # Save results
        cv2.imwrite("../outputs/classic_cartoon.jpg", classic)
        cv2.imwrite("../outputs/smooth_cartoon.jpg", smooth)
        cv2.imwrite("../outputs/edge_heavy_cartoon.jpg", edge_heavy)
        cv2.imwrite("../outputs/pencil_sketch.jpg", pencil)
        cv2.imwrite("../outputs/oil_painting.jpg", oil)
        
        print("✅ Cartoon conversions saved to outputs folder!")
    else:
        print(f"⚠️  Test image not found at {test_image_path}")
        print("Available styles:", converter.get_available_styles())
