"""
watermark-sismul-dct
====================

DCT-based invisible image watermarking library for JPEG robustness evaluation.

This library provides tools for embedding and extracting invisible watermarks
in the DCT (Discrete Cosine Transform) domain using mid-frequency coefficients.

Features:
  - DCT-based watermark embedding and extraction
  - JPEG compression robustness testing
  - Bit Error Rate (BER) evaluation
  - Support for binary watermark patterns
  
Quick start:
  >>> from watermark_sismul import WatermarkEncoder, WatermarkDecoder
  >>> from watermark_sismul import create_binary_watermark
  >>> import numpy as np
  >>> 
  >>> # Create watermark
  >>> wm = create_binary_watermark(size=16, pattern='x')
  >>> 
  >>> # Embed
  >>> encoder = WatermarkEncoder(alpha=25)
  >>> watermarked = encoder.encode(image, wm)
  >>> 
  >>> # Extract
  >>> decoder = WatermarkDecoder()
  >>> extracted = decoder.decode(watermarked, len(wm))
"""

__version__ = '0.1.0'
__author__ = 'Watermarking Research Team'
__license__ = 'MIT'

from .encoder import WatermarkEncoder, create_binary_watermark
from .decoder import WatermarkDecoder, compute_ber, evaluate_robustness, bits_to_text
from .dct import dct2, idct2

__all__ = [
    'WatermarkEncoder',
    'WatermarkDecoder',
    'create_binary_watermark',
    'compute_ber',
    'evaluate_robustness',
    'bits_to_text',
    'dct2',
    'idct2',
]
