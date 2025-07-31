"""
Setup script for Bioluminescent Detection AI Model

This package provides AI-powered distance prediction for bioluminescent bead detection
under various environmental conditions.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Bioluminescent Detection AI Model"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="bioluminescent-detection-ai",
    version="1.0.0",
    author="Lux Bio",
    author_email="info@luxbio.com",
    description="AI model for predicting bioluminescent bead detection distances",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/luxbio/bioluminescent-detection-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: Proprietary",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    python_requires=">=3.10",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "bioluminescence-ai=bioluminescence_model:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml"],
    },
    keywords=[
        "bioluminescence",
        "detection",
        "distance",
        "prediction",
        "AI",
        "machine learning",
        "drone",
        "search and rescue",
        "environmental modeling",
    ],
    project_urls={
        "Bug Reports": "https://github.com/luxbio/bioluminescent-detection-ai/issues",
        "Source": "https://github.com/luxbio/bioluminescent-detection-ai",
        "Documentation": "https://bioluminescent-detection-ai.readthedocs.io/",
    },
) 