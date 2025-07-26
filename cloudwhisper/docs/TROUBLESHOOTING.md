# CloudWhisper Troubleshooting Guide

## Table of Contents
1. [Common Installation Issues](#common-installation-issues)
2. [Configuration Problems](#configuration-problems)
3. [AWS-Related Issues](#aws-related-issues)
4. [OpenAI API Issues](#openai-api-issues)
5. [Runtime Errors](#runtime-errors)
6. [Performance Issues](#performance-issues)
7. [Debug Mode](#debug-mode)
8. [Getting Help](#getting-help)

## Common Installation Issues

### Issue: Python Version Incompatibility

**Symptoms:**
```
ERROR: Package requires a different Python: 3.7.0 not in '>=3.8'
```

**Cause:** CloudWhisper requires Python 3.8 or higher.

**Solution:**
```bash
# Check current Python version
python3 --version

# Install Python 3.8+ (Ubuntu/Debian)
sudo apt update
sudo apt install python3.8 python3.8-venv python3.8-pip

# Create virtual environment with correct Python version
python3.8 -m venv venv
source venv/bin/activate
pip install -e .
```

### Issue: pip Installation Fails

**Symptoms:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Cause:** Insufficient permissions or system-wide installation attempt.

**Solution:**
```bash
# Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Or install for user only
pip install --user -e .

# Upgrade pip if needed
python3 -m pip install --upgrade pip
```

### Issue: Virtual Environment Creation Fails

**Symptoms:**
```
The virtual environment was not created successfully because ensurepip is not available
```

**Cause:** Missing venv package.

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# CentOS/RHEL
sudo yum install python3-venv

# macOS (using Homebrew)
brew install python3

# Then create virtual environment
python3 -m venv venv
```

### Issue: SSL Certificate Errors

**Symptoms:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Cause:** Outdated certificates or corporate firewall.

**Solution:**
```bash
# Upgrade certificates
pip install --upgrade certifi

# Install with trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org -e .

# For corporate environments, configure proxy
pip install --proxy http://proxy.company.com:8080 -e .
```

## Configuration Problems

### Issue: AWS Credentials Not Found

**Symptoms:**
```
Unable to locate credentials. You can configure credentials by running "aws configure".
```

**Cause:** AWS credentials not configured.

**Solution:**
```bash
# Method 1: AWS CLI configuration
aws configure
# Enter your AWS Access Key ID, Secret Access Key, region, and output format

# Method 2: Environment variables
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1

# Method 3: AWS credentials file
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = your_access_key_id
aws_secret_access_key = your_secret_access_key
EOF

cat > ~/.aws/config << EOF
[default]
region = us-east-1
output = json
EOF

# Verify configuration
aws sts get-caller-identity
```

### Issue: OpenAI API Key Missing

**Symptoms:**
```
OpenAI API key is required. Set OPENAI_API_KEY environment variable.
```

**Cause:** OpenAI API key not configured.

**Solution:**
```bash
# Set environment variable
export OPENAI_API_KEY=your_openai_api_key

# Make it persistent (add to ~/.bashrc or ~/.zshrc)
echo 'export OPENAI_API_KEY=your_openai_api_key' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $OPENAI_API_KEY
```

### Issue: Wrong AWS Region

**Symptoms:**
```
An error occurred (InvalidAction) when calling the GetCostAndUsage operation
```

**Cause:** Cost Explorer is only available in us-east-1.

**Solution:**
```bash
# Cost Explorer requires us-east-1
export AWS_DEFAULT_REGION=us-east-1

# Or specify region in commands
cloudwhisper analyze-costs --days 7
```

## AWS-Related Issues

### Issue: Insufficient Permissions

**Symptoms:**
```
An error occurred (AccessDenied) when calling the GetCostAndUsage operation
```

**Cause:** AWS user/role lacks necessary permissions.

**Solution:**
Create an IAM policy with required permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetUsageReport",
                "ce:GetSavingsPlansUtilization",
                "ce:GetReservationCoverage",
                "ce:GetReservationPurchaseRecommendation",
                "ce:GetSavingsPlansRecommendations",
                "ec2:DescribeInstances",
                "ec2:DescribeVolumes",
                "ec2:DescribeAddresses",
                "cloudwatch:GetMetricStatistics",
                "s3:ListAllMyBuckets",
                "s3:GetBucketLocation",
                "s3:GetBucketLifecycleConfiguration",
                "rds:DescribeDBInstances",
                "elbv2:DescribeLoadBalancers",
                "elbv2:DescribeTargetGroups",
                "elbv2:DescribeTargetHealth",
                "compute-optimizer:GetEC2InstanceRecommendations"
            ],
            "Resource": "*"
        }
    ]
}
```

Attach this policy to your IAM user or role.

### Issue: Cost Explorer Not Enabled

**Symptoms:**
```
Cost Explorer is not available in your account
```

**Cause:** Cost Explorer not enabled in AWS account.

**Solution:**
1. Log into AWS Console
2. Go to Billing & Cost Management
3. Navigate to Cost Explorer
4. Click "Enable Cost Explorer"
5. Wait up to 24 hours for data to be available

### Issue: No Cost Data Available

**Symptoms:**
```
No cost data found for the specified period
```

**Cause:** No costs incurred or Cost Explorer data not ready.

**Solution:**
```bash
# Try a longer time period
cloudwhisper analyze-costs --days 30

# Check if you have any AWS resources
aws ec2 describe-instances
aws s3 ls

# Verify Cost Explorer has data
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-02 \
  --granularity DAILY \
  --metrics BlendedCost
```

### Issue: Rate Limiting

**Symptoms:**
```
An error occurred (Throttling) when calling the GetCostAndUsage operation
```

**Cause:** Too many API calls in short time.

**Solution:**
```bash
# Wait and retry
sleep 60
cloudwhisper analyze-costs --days 7

# Use longer time periods to reduce API calls
cloudwhisper analyze-costs --days 30 --granularity MONTHLY
```

## OpenAI API Issues

### Issue: Invalid API Key

**Symptoms:**
```
Incorrect API key provided
```

**Cause:** Invalid or expired OpenAI API key.

**Solution:**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Update environment variable:
```bash
export OPENAI_API_KEY=your_new_api_key
```

### Issue: API Quota Exceeded

**Symptoms:**
```
You exceeded your current quota, please check your plan and billing details
```

**Cause:** OpenAI API usage limits exceeded.

**Solution:**
1. Check your OpenAI usage at https://platform.openai.com/usage
2. Upgrade your plan if needed
3. Wait for quota reset if on free tier

### Issue: Model Not Available

**Symptoms:**
```
The model 'gpt-4' does not exist
```

**Cause:** Model not available for your API key.

**Solution:**
```bash
# Use GPT-3.5 instead (modify configuration)
export OPENAI_MODEL=gpt-3.5-turbo

# Or check available models
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## Runtime Errors

### Issue: Command Not Found

**Symptoms:**
```
cloudwhisper: command not found
```

**Cause:** CloudWhisper not installed or virtual environment not activated.

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Verify installation
pip list | grep cloudwhisper

# Reinstall if necessary
pip install -e .

# Check PATH
which cloudwhisper
```

### Issue: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'cloudwhisper'
```

**Cause:** Package not installed or wrong Python environment.

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall package
pip uninstall cloudwhisper
pip install -e .
```

### Issue: Timeout Errors

**Symptoms:**
```
Request timed out
```

**Cause:** Network issues or slow API responses.

**Solution:**
```bash
# Check internet connectivity
ping api.openai.com
ping aws.amazon.com

# Try with shorter time periods
cloudwhisper analyze-costs --days 7

# Check proxy settings if in corporate environment
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

### Issue: Memory Errors

**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Cause:** Large datasets or insufficient memory.

**Solution:**
```bash
# Use shorter time periods
cloudwhisper analyze-costs --days 7 --granularity DAILY

# Use monthly granularity for longer periods
cloudwhisper analyze-costs --days 90 --granularity MONTHLY

# Analyze specific services
cloudwhisper analyze-costs --service ec2 --days 30
```

## Performance Issues

### Issue: Slow Response Times

**Symptoms:** Commands take very long to complete.

**Cause:** Large datasets, network latency, or API rate limits.

**Solution:**
```bash
# Use appropriate granularity
# For < 30 days, use DAILY
cloudwhisper analyze-costs --days 14 --granularity DAILY

# For > 30 days, use MONTHLY
cloudwhisper analyze-costs --days 90 --granularity MONTHLY

# Analyze specific services
cloudwhisper analyze-costs --service ec2 --days 30

# Use specific regions
cloudwhisper optimize --service ec2 --region us-east-1
```

### Issue: High API Costs

**Symptoms:** Unexpected OpenAI API charges.

**Cause:** Frequent or complex Terraform generation requests.

**Solution:**
```bash
# Be specific in requests to reduce token usage
cloudwhisper generate "Create S3 bucket with versioning" # Good
# Instead of: "Create storage solution" # Too vague

# Save generated code to avoid regeneration
cloudwhisper generate "Create VPC" -o vpc.tf

# Review generated code before regenerating
cat vpc.tf
```

## Debug Mode

### Enable Debug Logging

```bash
# Enable debug mode
export CLOUDWHISPER_DEBUG=1

# Run commands with verbose output
cloudwhisper analyze-costs --days 7

# Check specific modules
export CLOUDWHISPER_DEBUG_MODULE=infrawhisper
cloudwhisper generate "Create S3 bucket"
```

### Debug AWS API Calls

```bash
# Enable AWS CLI debug
export AWS_DEBUG=1

# Test AWS connectivity
aws sts get-caller-identity

# Test Cost Explorer
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-02 \
  --granularity DAILY \
  --metrics BlendedCost
```

### Debug OpenAI API Calls

```bash
# Test OpenAI API directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Test chat completion
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
  }'
```

### Check System Resources

```bash
# Check memory usage
free -h

# Check disk space
df -h

# Check network connectivity
ping -c 4 api.openai.com
ping -c 4 aws.amazon.com

# Check DNS resolution
nslookup api.openai.com
nslookup aws.amazon.com
```

## Getting Help

### Self-Diagnosis Checklist

Before seeking help, check:

1. **Python version**: `python3 --version` (should be 3.8+)
2. **Virtual environment**: `which python` (should point to venv)
3. **Package installation**: `pip list | grep cloudwhisper`
4. **AWS credentials**: `aws sts get-caller-identity`
5. **OpenAI API key**: `echo $OPENAI_API_KEY`
6. **Internet connectivity**: `ping api.openai.com`
7. **Permissions**: Try with minimal commands first

### Collect Debug Information

```bash
# System information
uname -a
python3 --version
pip --version

# CloudWhisper information
cloudwhisper --version
pip show cloudwhisper

# AWS configuration
aws configure list
aws sts get-caller-identity

# Environment variables
env | grep -E "(AWS|OPENAI|CLOUDWHISPER)"

# Test basic functionality
cloudwhisper --help
```

### Common Solutions Summary

| Issue | Quick Fix |
|-------|-----------|
| Command not found | `source venv/bin/activate` |
| AWS credentials | `aws configure` |
| OpenAI API key | `export OPENAI_API_KEY=your_key` |
| Permission denied | Use virtual environment |
| SSL errors | `pip install --upgrade certifi` |
| Timeout | Check network, use shorter periods |
| No cost data | Enable Cost Explorer, wait 24h |
| Rate limiting | Wait and retry with longer periods |

### When to Seek Help

Create a GitHub issue if:
- You've followed all troubleshooting steps
- The issue is reproducible
- You have debug information ready
- The issue affects core functionality

Include in your issue:
- Operating system and Python version
- Complete error message
- Steps to reproduce
- Debug output (with sensitive info removed)
- CloudWhisper version

### Community Resources

- GitHub Issues: Report bugs and feature requests
- Documentation: Check all docs files
- Examples: Review examples for proper usage
- Stack Overflow: Tag questions with `cloudwhisper`

This troubleshooting guide should help you resolve most common issues with CloudWhisper. If you encounter problems not covered here, please create an issue with detailed information.
