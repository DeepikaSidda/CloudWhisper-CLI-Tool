.PHONY: install install-dev test lint format clean build upload help

# Default target
help:
	@echo "CloudWhisper Development Commands"
	@echo "================================="
	@echo "install      - Install the package in development mode"
	@echo "install-dev  - Install with development dependencies"
	@echo "test         - Run tests"
	@echo "lint         - Run linting checks"
	@echo "format       - Format code with black"
	@echo "clean        - Clean build artifacts"
	@echo "build        - Build distribution packages"
	@echo "upload       - Upload to PyPI (requires credentials)"
	@echo "example      - Run usage examples"

# Install the package in development mode
install:
	pip install -e .

# Install with development dependencies
install-dev:
	pip install -e ".[dev]"
	pip install -r requirements.txt

# Run tests (when test files are created)
test:
	python -m pytest tests/ -v

# Run linting checks
lint:
	flake8 cloudwhisper/
	mypy cloudwhisper/

# Format code with black
format:
	black cloudwhisper/
	black examples/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build distribution packages
build: clean
	python setup.py sdist bdist_wheel

# Upload to PyPI (requires twine and credentials)
upload: build
	twine upload dist/*

# Run usage examples
example:
	python examples/usage_examples.py

# Setup development environment
setup-dev: install-dev
	@echo "Development environment setup complete!"
	@echo "Make sure to set the following environment variables:"
	@echo "  export AWS_ACCESS_KEY_ID=your_access_key"
	@echo "  export AWS_SECRET_ACCESS_KEY=your_secret_key"
	@echo "  export AWS_DEFAULT_REGION=us-east-1"
	@echo "  export OPENAI_API_KEY=your_openai_key"

# Check if CLI is working
check:
	cloudwhisper --help
