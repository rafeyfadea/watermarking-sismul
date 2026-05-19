"""Basic tests for watermark_sismul package."""

import numpy as np
import pytest
from watermark_sismul import (
    WatermarkEncoder,
    WatermarkDecoder,
    create_binary_watermark,
    compute_ber,
    dct2,
    idct2,
)


class TestDCT:
    """Test DCT and IDCT functions."""
    
    def test_dct2_shape(self):
        """Test DCT output shape."""
        block = np.random.randn(8, 8)
        result = dct2(block)
        assert result.shape == block.shape
    
    def test_idct2_reconstruction(self):
        """Test IDCT reconstruction."""
        block = np.random.randn(8, 8)
        dct_result = dct2(block)
        reconstructed = idct2(dct_result)
        # Allow small numerical error
        assert np.allclose(block, reconstructed, atol=1e-10)


class TestWatermarkCreation:
    """Test watermark pattern creation."""
    
    def test_pattern_x(self):
        """Test X pattern creation."""
        wm = create_binary_watermark(size=4, pattern='x')
        assert len(wm) == 16
        assert wm.sum() == 6  # 4 diagonal + 4 anti-diagonal - 2 center overlap
    
    def test_pattern_h(self):
        """Test horizontal stripes."""
        wm = create_binary_watermark(size=4, pattern='h')
        assert len(wm) == 16
        assert wm.sum() == 8  # 2 rows of 4
    
    def test_pattern_v(self):
        """Test vertical stripes."""
        wm = create_binary_watermark(size=4, pattern='v')
        assert len(wm) == 16
        assert wm.sum() == 8  # 2 columns of 4


class TestEncoder:
    """Test watermark embedding."""
    
    def test_encode_basic(self):
        """Test basic embedding."""
        img = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        wm = create_binary_watermark(size=8, pattern='x')
        
        encoder = WatermarkEncoder()
        watermarked = encoder.encode(img, wm)
        
        assert watermarked.shape == img.shape
        assert watermarked.dtype == np.uint8
        assert not np.array_equal(img, watermarked)  # Changed
    
    def test_encode_alpha_effect(self):
        """Test that higher alpha produces larger changes."""
        img = np.ones((64, 64), dtype=np.uint8) * 128
        wm = np.ones(64)
        
        encoder1 = WatermarkEncoder(alpha=10)
        encoder2 = WatermarkEncoder(alpha=50)
        
        w1 = encoder1.encode(img, wm)
        w2 = encoder2.encode(img, wm)
        
        diff1 = np.abs(img.astype(float) - w1.astype(float)).sum()
        diff2 = np.abs(img.astype(float) - w2.astype(float)).sum()
        
        assert diff2 > diff1  # Larger alpha → more change


class TestDecoder:
    """Test watermark extraction."""
    
    def test_decode_perfect(self):
        """Test extraction from unwatermarked image."""
        img = np.random.randint(50, 200, (64, 64), dtype=np.uint8)
        wm = create_binary_watermark(size=8, pattern='x')
        
        encoder = WatermarkEncoder(alpha=25)
        watermarked = encoder.encode(img, wm)
        
        decoder = WatermarkDecoder()
        extracted = decoder.decode(watermarked, len(wm))
        
        ber = compute_ber(wm, extracted)
        assert ber == 0.0  # Perfect extraction without attack
    
    def test_decode_shape(self):
        """Test extracted bits shape."""
        img = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
        wm = np.random.randint(0, 2, 32)
        
        encoder = WatermarkEncoder()
        watermarked = encoder.encode(img, wm)
        
        decoder = WatermarkDecoder()
        extracted = decoder.decode(watermarked, len(wm))
        
        assert len(extracted) == len(wm)
        assert extracted.dtype == int
        assert np.all((extracted == 0) | (extracted == 1))


class TestBER:
    """Test Bit Error Rate computation."""
    
    def test_ber_perfect(self):
        """Test BER for identical bits."""
        orig = np.array([1, 0, 1, 0, 1, 1, 0, 0])
        ext = np.array([1, 0, 1, 0, 1, 1, 0, 0])
        
        assert compute_ber(orig, ext) == 0.0
    
    def test_ber_all_wrong(self):
        """Test BER for all wrong bits."""
        orig = np.array([1, 0, 1, 0])
        ext = np.array([0, 1, 0, 1])
        
        assert compute_ber(orig, ext) == 1.0
    
    def test_ber_half_wrong(self):
        """Test BER for half wrong bits."""
        orig = np.array([1, 1, 0, 0])
        ext = np.array([1, 0, 0, 1])
        
        assert compute_ber(orig, ext) == 0.5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
