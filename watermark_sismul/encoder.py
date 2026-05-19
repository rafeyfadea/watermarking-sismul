"""
Watermark encoder for DCT-based invisible watermarking.

Embeds binary watermark data into image blocks using DCT coefficients.
Mid-frequency positions [1,2] and [2,1] are used to balance robustness and imperceptibility.
"""

import numpy as np
from PIL import Image
import io
from .dct import dct2, idct2


class WatermarkEncoder:
    """
    Encode watermarks into images using DCT domain embedding.
    
    The embedding uses a comparative method:
    - Bit 1: Strengthen coefficient [1,2], keep [2,1]
    - Bit 0: Strengthen coefficient [2,1], keep [1,2]
    
    During extraction, the bit is determined by comparing magnitudes.
    """
    
    def __init__(self, block_size: int = 8, alpha: float = 25.0):
        """
        Initialize the watermark encoder.
        
        Args:
            block_size: Size of image blocks for DCT (default 8 for JPEG compatibility)
            alpha: Embedding strength (default 25, higher = stronger but more visible)
        """
        self.block_size = block_size
        self.alpha = alpha
        
    def encode(self, image: np.ndarray, watermark_bits: np.ndarray) -> np.ndarray:
        """
        Embed watermark into image using DCT.
        
        Args:
            image: Input image (grayscale as uint8 or float64)
            watermark_bits: Binary watermark data (1D array of 0s and 1s)
            
        Returns:
            Watermarked image (uint8)
            
        Example:
            >>> encoder = WatermarkEncoder(alpha=25)
            >>> wm = np.array([1, 0, 1, 0, ...])
            >>> watermarked = encoder.encode(image, wm)
        """
        img = image.astype(float)
        H, W = img.shape
        out = img.copy()
        idx = 0
        for r in range(0, H-7, 8):
            for c in range(0, W-7, 8):
                if idx >= len(watermark_bits):
                    break
                blk = img[r:r+8, c:c+8] - 128
                D = dct2(blk)
                if watermark_bits[idx] == 1:
                    D[1,2] = abs(D[1,2]) + self.alpha
                    D[2,1] = abs(D[2,1])
                else:
                    D[1,2] = abs(D[1,2])
                    D[2,1] = abs(D[2,1]) + self.alpha
                out[r:r+8, c:c+8] = np.clip(idct2(D)+128, 0, 255)
                idx += 1
        return out.astype(np.uint8)
    
    def encode_from_file(self, image_path: str, watermark_bits: np.ndarray,
                        output_path: str, convert_to_grayscale: bool = True) -> str:
        """
        Encode watermark from an image file and save to disk.
        
        Args:
            image_path: Path to input image
            watermark_bits: Binary watermark data
            output_path: Path to save watermarked image
            convert_to_grayscale: If True, convert to grayscale (default True)
            
        Returns:
            Path to saved watermarked image
        """
        # Load image
        img = Image.open(image_path)
        if convert_to_grayscale:
            img = img.convert('L')
        img_array = np.array(img)
        
        # Encode
        watermarked = self.encode(img_array, watermark_bits)
        
        # Save
        Image.fromarray(watermarked).save(output_path)
        return output_path


def create_binary_watermark(size: int = 16) -> np.ndarray:
    """
    Create a binary watermark with X pattern (from notebook).
    
    Creates a watermark matrix with diagonal cross pattern:
    - Main diagonal = 1
    - Anti-diagonal = 1
    - Rest = 0
    
    Args:
        size: Size of 2D watermark matrix (default 16)
        
    Returns:
        1D array of watermark bits
        
    Example:
        >>> wm = create_binary_watermark(size=16)
        >>> print(f"Watermark: {len(wm)} bits, {wm.sum()} active")
    """
    wm = np.zeros((size, size), dtype=int)
    for i in range(size):
        wm[i, i] = 1
        wm[i, size-1-i] = 1
    return wm.flatten()
