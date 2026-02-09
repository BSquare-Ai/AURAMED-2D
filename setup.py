"""
Setup script for I-AURA-MED2D
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="i-aura-med2d",
    version="0.1.0",
    description="An Agentic Unification of Reasoning & Embodied Abstraction Architecture for 2D Medical Images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="I-AURA-MED2D Team",
    author_email="",
    url="https://github.com/your-org/I-AURA-MED2D",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "numpy>=1.21.0",
        "Pillow>=9.0.0",
        "opencv-python>=4.5.0",
        "monai>=1.0.0",
        "transformers>=4.30.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "api": ["flask>=2.3.0", "fastapi>=0.100.0", "uvicorn>=0.23.0"],
        "dev": ["pytest>=7.3.0", "black>=23.0.0", "flake8>=6.0.0"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

