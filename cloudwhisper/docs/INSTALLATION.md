# CloudWhisper Installation Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [Uninstallation](#uninstallation)

## System Requirements

### Operating System
- Linux (Ubuntu 18.04+, CentOS 7+, Amazon Linux 2)
- macOS 10.14+
- Windows 10+ (with WSL2 recommended)

### Python
- Python 3.8 or higher
- pip package manager
- Virtual environment support (recommended)

### Dependencies
- AWS CLI (optional but recommended)
- Git (for source installation)

### Network Requirements
- Internet access for:
  - OpenAI API calls
  - AWS API calls
  - Package downloads

## Installation Methods

### Method 1: Install from Source (Recommended)

This method gives you the latest version and allows for easy customization.

#### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/cloudwhisper.git
cd cloudwhisper
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install the package in development mode
pip install -e .
```

#### Step 4: Verify Installation
```bash
cloudwhisper --version
cloudwhisper --help
```

### Method 2: Install from PyPI (When Available)

```bash
# Create virtual environment (recommended)
python3 -m venv cloudwhisper-env
source cloudwhisper-env/bin/activate  # On Windows: cloudwhisper-env\Scripts\activate

# Install from PyPI
pip install cloudwhisper

# Verify installation
cloudwhisper --version
```

### Method 3: Install with pipx (Isolated Installation)

```bash
# Install pipx if not already installed
pip install --user pipx
pipx ensurepath

# Install CloudWhisper
pipx install cloudwhisper

# Verify installation
cloudwhisper --version
```

### Method 4: Docker Installation (Coming Soon)

```bash
# Pull the Docker image
docker pull cloudwhisper/cloudwhisper:latest

# Run CloudWhisper in a container
docker run -it --rm \
  -e AWS_ACCESS_KEY_ID=your_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret \
  -e OPENAI_API_KEY=your_openai_key \
  cloudwhisper/cloudwhisper:latest --help
```

## Configuration

### Step 1: AWS Configuration

#### Option A: Using AWS CLI (Recommended)
```bash
# Install AWS CLI if not already installed
pip install awscli

# Configure AWS credentials
aws configure
```

You'll be prompted to enter:
- AWS Access Key ID
- AWS Secret Access Key
- Default region name (e.g., us-east-1)
- Default output format (json recommended)

#### Option B: Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1
```

#### Option C: IAM Roles (For EC2/ECS/Lambda)
If running on AWS infrastructure, you can use IAM roles instead of access keys.

### Step 2: OpenAI Configuration

Get your OpenAI API key from https://platform.openai.com/api-keys

```bash
export OPENAI_API_KEY=your_openai_api_key
```

### Step 3: Verify AWS Permissions

Ensure your AWS user/role has the necessary permissions:

```bash
# Test AWS connectivity
aws sts get-caller-identity

# Test Cost Explorer access
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-02 \
  --granularity DAILY \
  --metrics BlendedCost
```

### Step 4: Create Configuration File (Optional)

Create `~/.cloudwhisper/config.yaml`:

```bash
mkdir -p ~/.cloudwhisper
cat > ~/.cloudwhisper/config.yaml << EOF
# AWS Configuration
aws:
  default_region: us-east-1
  profile: default

# OpenAI Configuration
openai:
  api_key: ${OPENAI_API_KEY}
  model: gpt-4
  temperature: 0.1
  max_tokens: 2000

# Cost Analysis Settings
cost_analysis:
  default_days: 30
  default_granularity: DAILY
  currency: USD

# Optimization Settings
optimization:
  cpu_threshold_low: 10
  cpu_threshold_high: 80
  idle_days_threshold: 7

# Terraform Settings
terraform:
  default_provider_version: "~> 5.0"
  include_tags: true
  default_tags:
    Environment: dev
    ManagedBy: CloudWhisper
    Project: infrastructure
EOF
```

## Verification

### Basic Functionality Test

```bash
# Test CLI is working
cloudwhisper --help

# Test AWS connectivity (should not error)
cloudwhisper analyze-costs --help

# Test OpenAI connectivity (requires API key)
cloudwhisper generate --help
```

### Full Integration Test

```bash
# Test cost analysis (requires AWS credentials)
cloudwhisper analyze-costs --days 7

# Test Terraform generation (requires OpenAI API key)
cloudwhisper generate "Create an S3 bucket"

# Test optimization recommendations
cloudwhisper optimize --help
```

### Run Test Suite

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest tests/
```

## Troubleshooting

### Common Installation Issues

#### Issue 1: Python Version Incompatibility
**Error:** `ERROR: Package requires a different Python`

**Solution:**
```bash
# Check Python version
python3 --version

# Install Python 3.8+ if needed
# On Ubuntu:
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-pip

# Create virtual environment with specific Python version
python3.8 -m venv venv
```

#### Issue 2: pip Installation Fails
**Error:** `ERROR: Could not install packages due to an EnvironmentError`

**Solution:**
```bash
# Upgrade pip
python3 -m pip install --upgrade pip

# Install with user flag
pip install --user -e .

# Or use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

#### Issue 3: Virtual Environment Issues
**Error:** `command not found: python3 -m venv`

**Solution:**
```bash
# On Ubuntu/Debian:
sudo apt install python3-venv

# On CentOS/RHEL:
sudo yum install python3-venv

# On macOS:
brew install python3
```

#### Issue 4: Permission Denied
**Error:** `PermissionError: [Errno 13] Permission denied`

**Solution:**
```bash
# Don't use sudo with pip, use virtual environment instead
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

#### Issue 5: SSL Certificate Issues
**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution:**
```bash
# Upgrade certificates
pip install --upgrade certifi

# Or install with trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org -e .
```

### Configuration Issues

#### Issue 1: AWS Credentials Not Found
**Error:** `Unable to locate credentials`

**Solution:**
```bash
# Check AWS configuration
aws configure list

# Set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Or configure AWS CLI
aws configure
```

#### Issue 2: OpenAI API Key Missing
**Error:** `OpenAI API key is required`

**Solution:**
```bash
# Set environment variable
export OPENAI_API_KEY=your_openai_api_key

# Add to shell profile for persistence
echo 'export OPENAI_API_KEY=your_openai_api_key' >> ~/.bashrc
source ~/.bashrc
```

#### Issue 3: Cost Explorer Not Available
**Error:** `Cost Explorer is not available in your account`

**Solution:**
1. Log into AWS Console
2. Go to Billing & Cost Management
3. Navigate to Cost Explorer
4. Click "Enable Cost Explorer"
5. Wait up to 24 hours for data to be available

### Runtime Issues

#### Issue 1: Import Errors
**Error:** `ModuleNotFoundError: No module named 'cloudwhisper'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall in development mode
pip install -e .

# Check installation
pip list | grep cloudwhisper
```

#### Issue 2: Command Not Found
**Error:** `cloudwhisper: command not found`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Check if command is installed
which cloudwhisper

# Reinstall if necessary
pip install -e .
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs:** Enable debug mode with `export CLOUDWHISPER_DEBUG=1`
2. **Verify prerequisites:** Ensure all system requirements are met
3. **Check permissions:** Verify AWS IAM permissions
4. **Test connectivity:** Ensure internet access to AWS and OpenAI APIs
5. **Create an issue:** Report bugs on the GitHub repository

## Uninstallation

### Remove CloudWhisper

```bash
# If installed with pip
pip uninstall cloudwhisper

# If installed with pipx
pipx uninstall cloudwhisper

# Remove virtual environment (if used)
rm -rf venv/

# Remove configuration (optional)
rm -rf ~/.cloudwhisper/
```

### Clean Up Environment Variables

Remove from your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):
```bash
# Remove these lines
export OPENAI_API_KEY=your_openai_api_key
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1
```

## Next Steps

After successful installation:

1. **Read the User Guide:** `docs/USER_GUIDE.md`
2. **Check API Reference:** `docs/API_REFERENCE.md`
3. **Try Examples:** Run `python examples/usage_examples.py`
4. **Run Demo:** Execute `python demo.py`

## Support

For installation support:
- Check the troubleshooting section above
- Review system requirements
- Ensure all prerequisites are met
- Create an issue on GitHub with detailed error information

This installation guide should help you get CloudWhisper up and running on your system quickly and efficiently.
