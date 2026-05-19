# watermarking-sismul

DCT-based invisible image watermarking. Embed and extract hidden binary watermarks in the frequency domain, robust against JPEG compression.

![Python](https://img.shields.io/badge/python-3.7%2B-blue)

## Demo

| Original | Watermarked | Difference (10×) |
|:---:|:---:|:---:|
| ![original](images/original.png) | ![watermarked](images/watermarked.png) | ![difference](images/difference.png) |

The watermark is invisible to the human eye — hidden inside DCT frequency coefficients.

## Installation

```bash
git clone https://github.com/rafeyfadea/watermarking-sismul.git
cd watermark-sismul
pip install -e .
```

## How to Use with Your Own Image

```python
import numpy as np
from PIL import Image
from watermark_sismul import WatermarkEncoder, WatermarkDecoder, create_binary_watermark, compute_ber

# Load your image (change this path)
img = Image.open('your_photo.jpg').convert('L')
image = np.array(img)

# Create watermark
watermark = create_binary_watermark(size=16)  # 16×16 = 256 bits

# Embed
encoder = WatermarkEncoder(alpha=25)
watermarked = encoder.encode(image, watermark)
Image.fromarray(watermarked).save('result.jpg')

# Extract and verify
decoder = WatermarkDecoder()
extracted = decoder.decode(watermarked, len(watermark))
ber = compute_ber(watermark, extracted)
print(f"BER: {ber:.4f} — {'OK' if ber <= 0.3 else 'FAIL'}")
```

Replace `'your_photo.jpg'` with any image file. The output `result.jpg` contains the hidden watermark.

## JPEG Robustness Test

```python
from watermark_sismul import evaluate_robustness

results = evaluate_robustness(watermarked, watermark, quality_factors=[10, 30, 50, 70, 90])
for qf, res in results.items():
    print(f"QF {qf:3d} | BER={res['ber']:.4f} | {'PASS' if res['success'] else 'FAIL'}")
```

## Parameters

| Parameter | Default | Effect |
|-----------|---------|--------|
| `alpha` | `25.0` | Embedding strength — higher = more robust, less invisible |
| `size` | `16` | Watermark size (16 → 256 bits, must fit image blocks) |
