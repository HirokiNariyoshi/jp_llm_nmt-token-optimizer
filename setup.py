from setuptools import setup, find_packages

setup(
    name="token_optimizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "tiktoken>=0.5.0",
        "python-dotenv>=1.0.0",
        "transformers>=4.30.0",
        "sentencepiece>=0.1.99",
        "torch>=2.0.0",
    ],
)
