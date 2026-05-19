#!/usr/bin/env python
"""
Example: Embed and extract watermark with robustness testing.

This example demonstrates:
1. Loading an image
2. Creating a binary watermark
3. Embedding the watermark
4. Extracting it from different JPEG quality levels
5. Computing Bit Error Rate (BER)
"""

import numpy as np
from PIL import Image
import sys

try:
    from watermark_sismul import (
        WatermarkEncoder,
        WatermarkDecoder,
        create_binary_watermark,
        compute_ber,
        evaluate_robustness
    )
except ImportError:
    print("Error: watermark_sismul not installed.")
    print("Install with: pip install -e ..")
    sys.exit(1)


def example_basic():
    """Basic embed/extract example with a generated test image."""
    print("=" * 60)
    print("Example 1: Basic Embed and Extract")
    print("=" * 60)
    
    # Create a test image (64x64 grayscale)
    test_image = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
    print(f"Created test image: {test_image.shape}")
    
    # Create watermark (16x16 pattern = 256 bits, but 64x64 image has only 64 blocks)
    wm = create_binary_watermark(size=16, pattern='x')
    print(f"Created watermark: {len(wm)} bits ({wm.sum()} active bits)")
    print(f"First 64 bits (used): {wm[:64]}")
    
    # Embed
    encoder = WatermarkEncoder(alpha=25)
    watermarked = encoder.encode(test_image, wm)
    print(f"\nEmbedded watermark (alpha=25)")
    print(f"Image range before: [{test_image.min()}, {test_image.max()}]")
    print(f"Image range after:  [{watermarked.min()}, {watermarked.max()}]")
    print(f"Max pixel difference: {np.abs(test_image.astype(int) - watermarked).max()}")
    
    # Extract
    decoder = WatermarkDecoder()
    extracted = decoder.decode(watermarked, len(wm))
    print(f"\nExtracted watermark: {len(extracted)} bits")
    
    # Compare
    ber = compute_ber(wm, extracted)
    print(f"BER (perfect conditions): {ber:.4f}")
    print(f"Extraction successful: {'✓ YES' if ber == 0 else '✗ NO'}")


def example_with_file():
    """Example using actual image file (if available)."""
    print("\n" + "=" * 60)
    print("Example 2: File-based Embed/Extract")
    print("=" * 60)
    
    image_path = 'test_image.jpg'
    
    # Check if test image exists
    try:
        img = Image.open(image_path)
        print(f"Loaded image: {image_path} - {img.size}")
        
        # Convert to grayscale
        img_gray = img.convert('L').resize((64, 64))
        print(f"Resized to: {img_gray.size}")
        
        # Create watermark from text
        text = "SISMUL"
        wm = np.array([int(b) for b in ''.join(format(ord(c), '08b') for c in text)])
        print(f"Text watermark: '{text}' ({len(wm)} bits)")
        
        # Embed and save
        encoder = WatermarkEncoder(alpha=25)
        watermarked = encoder.encode_from_file(
            image_path,
            wm,
            'watermarked.jpg',
            convert_to_grayscale=True
        )
        print(f"Saved watermarked image: {watermarked}")
        
        # Extract
        decoder = WatermarkDecoder()
        extracted = decoder.decode_from_file(watermarked, len(wm))
        print(f"Extracted bits: {extracted}")
        
    except FileNotFoundError:
        print(f"Note: {image_path} not found. Skipping file-based example.")
        print("To run this, provide a test image in the current directory.")


def example_robustness():
    """Example: Test robustness against JPEG compression."""
    print("\n" + "=" * 60)
    print("Example 3: JPEG Robustness Testing")
    print("=" * 60)
    
    # Create test image and watermark
    test_image = np.random.randint(50, 200, (64, 64), dtype=np.uint8)
    wm = create_binary_watermark(size=16, pattern='x')
    
    # Embed
    encoder = WatermarkEncoder(alpha=25)
    watermarked = encoder.encode(test_image, wm)
    
    # Test robustness
    print("Testing robustness against JPEG compression...")
    quality_factors = [10, 30, 50, 70, 90]
    
    decoder = WatermarkDecoder()
    results = decoder.evaluate_robustness(watermarked, wm, quality_factors)
    
    # Print results
    print(f"\n{'QF':>5} | {'BER':>8} | {'Errors':>8} | Status")
    print("-" * 40)
    for qf in quality_factors:
        res = results[qf]
        status = '✓ PASS' if res['success'] else '✗ FAIL'
        print(f"{qf:>5} | {res['ber']:>8.4f} | {res['errors']:>8} | {status}")
    
    # Summary
    success_count = sum(1 for r in results.values() if r['success'])
    print(f"\nRobustness: {success_count}/{len(quality_factors)} quality levels passed")


if __name__ == '__main__':
    example_basic()
    example_with_file()
    example_robustness()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
