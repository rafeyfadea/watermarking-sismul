"""Setup configuration for watermark-sismul-dct package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="watermark-sismul-dct",
    version="0.1.0",
    author="Watermarking Research Team",
    author_email="",
    description="DCT-based invisible image watermarking library for JPEG robustness evaluation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/watermark-sismul-dct",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.19.0",
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "matplotlib>=3.3.0",
            "pytest-cov>=2.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "watermark-sismul=watermark_sismul.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="watermarking DCT JPEG image-processing robust-watermark",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/watermark-sismul-dct/issues",
        "Documentation": "https://github.com/yourusername/watermark-sismul-dct",
        "Source Code": "https://github.com/yourusername/watermark-sismul-dct",
    },
)
