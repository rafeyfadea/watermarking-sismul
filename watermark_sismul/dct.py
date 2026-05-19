"""
DCT (Discrete Cosine Transform) and IDCT implementation for image watermarking.

This module provides manual implementations of 2D DCT-II and IDCT transforms
without external DCT libraries. These are used for embedding and extracting
watermarks in the DCT domain.
"""

import numpy as np


def dct2(block: np.ndarray) -> np.ndarray:
    """
    Compute 2D Discrete Cosine Transform (DCT-II) of a block.
    
    Args:
        block: Input block (usually 8x8 from JPEG standard)
        
    Returns:
        DCT coefficients of the same shape
        
    Notes:
        - DC component at [0,0] (low frequency)
        - High frequencies at bottom-right
        - Mid-frequencies at [1,2] and [2,1] are suitable for watermark embedding
    """
    N = block.shape[0]
    result = np.zeros((N, N))
    
    for u in range(N):
        cu = (1 / np.sqrt(2)) if u == 0 else 1.0
        for v in range(N):
            cv = (1 / np.sqrt(2)) if v == 0 else 1.0
            s = 0.0
            for x in range(N):
                for y in range(N):
                    s += (block[x, y]
                          * np.cos((2*x + 1) * u * np.pi / (2 * N))
                          * np.cos((2*y + 1) * v * np.pi / (2 * N)))
            result[u, v] = (2 / N) * cu * cv * s
            
    return result


def idct2(block: np.ndarray) -> np.ndarray:
    """
    Compute 2D Inverse Discrete Cosine Transform (IDCT) of DCT coefficients.
    
    Args:
        block: DCT coefficients (usually 8x8)
        
    Returns:
        Reconstructed spatial domain block
        
    Notes:
        - Inverse operation of dct2()
        - Used to reconstruct image data after watermark embedding
    """
    N = block.shape[0]
    result = np.zeros((N, N))
    
    for x in range(N):
        for y in range(N):
            s = 0.0
            for u in range(N):
                cu = (1 / np.sqrt(2)) if u == 0 else 1.0
                for v in range(N):
                    cv = (1 / np.sqrt(2)) if v == 0 else 1.0
                    s += (cu * cv * block[u, v]
                          * np.cos((2*x + 1) * u * np.pi / (2 * N))
                          * np.cos((2*y + 1) * v * np.pi / (2 * N)))
            result[x, y] = (2 / N) * s
            
    return result
