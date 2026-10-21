from setuptools import setup, find_packages

setup(
    name="cloud-commanders",
    version="1.0.0",
    description="Python client SDK for Cloud Commanders & Version-Aware RAG Services",
    author="Cyber Knights",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "async": ["httpx>=0.24.0"],
        "dev": ["pytest", "pytest-mock"],
    },
    entry_points={
        "console_scripts": [
            "cloud-commanders=cloud_commanders.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
