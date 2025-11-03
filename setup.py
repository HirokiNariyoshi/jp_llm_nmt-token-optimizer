from setuptools import setup, find_packages

setup(
    name="token_optimizer",
    version="0.1.0",
    author="Hiroki Nariyoshi",
    description="Optimize Japanese LLM queries by translating to English",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "tiktoken>=0.5.0",
        "python-dotenv>=1.0.0",
        "transformers>=4.30.0",
        "sentencepiece>=0.1.99",
        "torch>=2.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
