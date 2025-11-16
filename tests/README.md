# Tests

This directory contains the test suite for the Token Optimizer.

## Running Tests

Install test dependencies:

```bash
pip install pytest pytest-cov
```

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=token_optimizer tests/
```

Run specific test file:

```bash
pytest tests/test_optimizer.py
```

## Test Structure

- `test_optimizer.py` - Core optimizer functionality tests
- `test_tokens.py` - Token counting and cost estimation tests

## Requirements

Tests require:

- Ollama running locally with llama3.2:3b model
- NLLB model downloaded (first test run will download it)

## Note

Some tests make actual API calls to Ollama, so they may take a few seconds to complete.
