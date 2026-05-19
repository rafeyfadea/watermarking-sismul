"""
Watermark decoder for extracting embedded watermarks from images.

Decodes watermarks embedded using the WatermarkEncoder by comparing DCT coefficients
and computing Bit Error Rate (BER) to evaluate robustness.
"""

import numpy as np
from PIL import Image
from .dct import dct2


class WatermarkDecoder:
    """
    Decode watermarks from watermarked images using DCT.
    
    Compares magnitudes at [1,2] and [2,1] to determine embedded bits:
    - If |D[1,2]| > |D[2,1]| → bit is 1
    - Otherwise → bit is 0
    """
    
    def __init__(self, block_size: int = 8):
        """
        Initialize the watermark decoder.
        
        Args:
            block_size: Size of image blocks for DCT (default 8 for JPEG compatibility)
        """
        self.block_size = block_size
        
    def decode(self, image: np.ndarray, n_bits: int) -> np.ndarray:
        """
        Extract watermark bits from image.
        
        Args:
            image: Input image (grayscale as uint8 or float64)
            n_bits: Number of bits to extract
            
        Returns:
            Extracted watermark bits (1D array of 0s and 1s)
            
        Example:
            >>> decoder = WatermarkDecoder()
            >>> extracted = decoder.decode(watermarked_image, 64)
            >>> print(f"Extracted: {extracted}")
        """
        img = image.astype(float)
        H, W = img.shape
        bits = []
        for r in range(0, H-7, 8):
            for c in range(0, W-7, 8):
                if len(bits) >= n_bits:
                    break
                D = dct2(img[r:r+8, c:c+8] - 128)
                bits.append(1 if abs(D[1,2]) > abs(D[2,1]) else 0)
        return np.array(bits)
    
    def decode_from_file(self, image_path: str, n_bits: int,
                        convert_to_grayscale: bool = True) -> np.ndarray:
        """
        Decode watermark from an image file.
        
        Args:
            image_path: Path to watermarked image
            n_bits: Number of bits to extract
            convert_to_grayscale: If True, convert to grayscale (default True)
            
        Returns:
            Extracted watermark bits
        """
        img = Image.open(image_path)
        if convert_to_grayscale:
            img = img.convert('L')
        img_array = np.array(img)
        
        return self.decode(img_array, n_bits)


def compute_ber(original_bits: np.ndarray, extracted_bits: np.ndarray) -> float:
    """
    Compute Bit Error Rate (BER) between original and extracted watermarks.
    
    BER = (number of incorrect bits) / (total bits)
    
    Args:
        original_bits: Original watermark bits
        extracted_bits: Extracted watermark bits
        
    Returns:
        BER as a float between 0 and 1
        
    Notes:
        - BER = 0: Perfect extraction
        - BER = 0.5: Random guess
        - BER > 0.3: Generally considered as failed extraction
    """
    n = min(len(original_bits), len(extracted_bits))
    return np.sum(original_bits[:n] != extracted_bits[:n]) / n


def evaluate_robustness(watermarked_image: np.ndarray, original_bits: np.ndarray,
                       quality_factors: list = [10, 30, 50, 70, 90]) -> dict:
    """
    Evaluate watermark robustness against JPEG compression at various quality factors.
    
    Args:
        watermarked_image: Watermarked image (grayscale)
        original_bits: Original watermark bits
        quality_factors: List of JPEG quality factors to test (default: [10, 30, 50, 70, 90])
        
    Returns:
        Dictionary with QF as key and {'ber': float, 'success': bool} as value
        Success is True if BER <= 0.3
        
    Example:
        >>> decoder = WatermarkDecoder()
        >>> results = decoder.evaluate_robustness(watermarked, watermark, [50, 75, 90])
        >>> for qf, res in results.items():
        ...     print(f"QF {qf}: BER={res['ber']:.4f}, Success={res['success']}")
    """
    import io
    
    decoder = WatermarkDecoder()
    results = {}
    
    for qf in quality_factors:
        # JPEG compress
        buf = io.BytesIO()
        Image.fromarray(watermarked_image).save(buf, format='JPEG', quality=qf)
        buf.seek(0)
        compressed = np.array(Image.open(buf).convert('L'))
        
        # Extract watermark
        extracted = decoder.decode(compressed, len(original_bits))
        
        # Compute BER
        ber_value = compute_ber(original_bits, extracted)
        success = ber_value <= 0.3
        
        results[qf] = {
            'ber': ber_value,
            'success': success,
            'errors': np.sum(original_bits != extracted[:len(original_bits)])
        }
        
    return results


def bits_to_text(bits: np.ndarray) -> str:
    """
    Convert binary array to text.
    
    Args:
        bits: 1D array of bits (length must be multiple of 8)
        
    Returns:
        Decoded text string
    """
    n = (len(bits) // 8) * 8
    text = ''
    for i in range(0, n, 8):
        byte = bits[i:i+8]
        text += chr(int(''.join(map(str, byte)), 2))
    return text
