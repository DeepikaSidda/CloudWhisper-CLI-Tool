# CloudWhisper User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Quick Start](#quick-start)
5. [Command Reference](#command-reference)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)

## Introduction

CloudWhisper is an AI-powered CLI tool designed to help AWS users manage infrastructure and optimize cloud costs through natural language interactions. It combines two powerful modules:

- **InfraWhisper**: Generate Terraform code from natural language descriptions
- **CloudFuel**: Analyze AWS costs and get optimization recommendations

### Key Features
- 🤖 AI-powered Terraform code generation using OpenAI GPT-4
- 💰 Comprehensive AWS cost analysis using Cost Explorer APIs
- 🔧 Intelligent optimization recommendations for EC2, S3, RDS, and more
- 🔍 Idle resource detection to eliminate waste
- 💡 Savings Plans recommendations
- 📊 Rich console output with tables and visualizations

## Installation

### Prerequisites
- Python 3.8 or higher
- AWS CLI configured with appropriate permissions
- OpenAI API key (for Terraform generation)

### Install from Source

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd cloudwhisper
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

4. **Verify installation:**
   ```bash
   cloudwhisper --help
   ```

### Install from PyPI (when available)
```bash
pip install cloudwhisper
```

## Configuration

### Environment Variables

Set up the following environment variables:

```bash
# AWS Configuration (required for cost analysis)
export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_DEFAULT_REGION=us-east-1

# OpenAI Configuration (required for Terraform generation)
export OPENAI_API_KEY=your_openai_api_key
```

### AWS Permissions

Your AWS user/role needs the following permissions:

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
                "ce:GetSavingsPlansUtilizationDetails",
                "ce:GetSavingsPlansUtilization",
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

### Configuration File (Optional)

Create `~/.cloudwhisper/config.yaml`:

```yaml
# AWS Configuration
aws:
  default_region: us-east-1
  profile: default

# OpenAI Configuration
openai:
  api_key: your_openai_api_key_here
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
```

## Quick Start

### 1. Generate Terraform Code
```bash
# Basic usage
cloudwhisper generate "Create an S3 bucket with versioning enabled"

# Save to file
cloudwhisper generate "Create a VPC with public and private subnets" -o vpc.tf

# Specify provider version
cloudwhisper generate "Launch an EC2 instance" --provider-version "~> 4.0"
```

### 2. Analyze Costs
```bash
# Analyze last 30 days
cloudwhisper analyze-costs

# Analyze specific service
cloudwhisper analyze-costs --service ec2 --days 7

# Group by dimensions
cloudwhisper analyze-costs --group-by SERVICE REGION --days 14
```

### 3. Get Optimization Recommendations
```bash
# General optimization recommendations
cloudwhisper optimize

# Service-specific optimization
cloudwhisper optimize --service ec2 --region us-east-1

# Find idle resources
cloudwhisper find-idle --days 7

# Get Savings Plans recommendations
cloudwhisper savings-plans
```

## Command Reference

### Global Options
- `--version`: Show version and exit
- `--help`: Show help message

### `generate` Command

Generate Terraform code from natural language description.

**Usage:**
```bash
cloudwhisper generate [OPTIONS] DESCRIPTION
```

**Options:**
- `-o, --output TEXT`: Output file for generated Terraform code
- `--provider-version TEXT`: AWS provider version (default: "~> 5.0")

**Examples:**
```bash
cloudwhisper generate "Create an S3 bucket with versioning and encryption"
cloudwhisper generate "Set up Auto Scaling Group with launch template" -o asg.tf
```

### `analyze-costs` Command

Analyze AWS costs and usage data.

**Usage:**
```bash
cloudwhisper analyze-costs [OPTIONS]
```

**Options:**
- `-d, --days INTEGER`: Number of days to analyze (default: 30)
- `-s, --service TEXT`: Specific AWS service to analyze
- `--granularity [DAILY|MONTHLY]`: Cost data granularity (default: DAILY)
- `--group-by [SERVICE|REGION|INSTANCE_TYPE|USAGE_TYPE]`: Group costs by dimension (multiple allowed)

**Examples:**
```bash
cloudwhisper analyze-costs --days 7
cloudwhisper analyze-costs --service ec2 --granularity MONTHLY
cloudwhisper analyze-costs --group-by SERVICE REGION --days 30
```

### `optimize` Command

Get cost optimization recommendations.

**Usage:**
```bash
cloudwhisper optimize [OPTIONS]
```

**Options:**
- `-s, --service TEXT`: Specific AWS service to optimize (ec2, s3, rds)
- `-r, --region TEXT`: Specific AWS region to analyze
- `-d, --days INTEGER`: Days of data to analyze for recommendations (default: 30)

**Examples:**
```bash
cloudwhisper optimize
cloudwhisper optimize --service ec2 --region us-west-2
cloudwhisper optimize --service s3 --days 60
```

### `find-idle` Command

Find idle AWS resources that can be terminated to save costs.

**Usage:**
```bash
cloudwhisper find-idle [OPTIONS]
```

**Options:**
- `-d, --days INTEGER`: Number of days to look back for idle resources (default: 7)
- `-r, --region TEXT`: Specific AWS region to analyze

**Examples:**
```bash
cloudwhisper find-idle
cloudwhisper find-idle --days 14 --region us-east-1
```

### `savings-plans` Command

Get Savings Plans recommendations.

**Usage:**
```bash
cloudwhisper savings-plans [OPTIONS]
```

**Examples:**
```bash
cloudwhisper savings-plans
```

## Examples

### Terraform Code Generation Examples

#### Basic Infrastructure
```bash
# S3 Bucket with features
cloudwhisper generate "Create an S3 bucket with versioning, encryption, and lifecycle policy"

# VPC Setup
cloudwhisper generate "Create a VPC with public and private subnets across 2 AZs with NAT gateway"

# EC2 Instance
cloudwhisper generate "Launch a t3.medium EC2 instance with security group allowing SSH and HTTP"
```

#### Advanced Infrastructure
```bash
# Load Balancer
cloudwhisper generate "Create Application Load Balancer with target groups and health checks"

# Auto Scaling
cloudwhisper generate "Set up Auto Scaling Group with launch template and scaling policies"

# Database
cloudwhisper generate "Create RDS MySQL instance with backup retention and encryption"

# Lambda Function
cloudwhisper generate "Create Python Lambda function with IAM role and CloudWatch logs"
```

### Cost Analysis Examples

#### Basic Cost Analysis
```bash
# Overall cost analysis
cloudwhisper analyze-costs --days 30

# Service-specific analysis
cloudwhisper analyze-costs --service ec2 --days 14
cloudwhisper analyze-costs --service s3 --days 7
```

#### Advanced Cost Analysis
```bash
# Multi-dimensional analysis
cloudwhisper analyze-costs --group-by SERVICE REGION --days 30

# Monthly granularity
cloudwhisper analyze-costs --granularity MONTHLY --days 90

# Specific service with grouping
cloudwhisper analyze-costs --service ec2 --group-by INSTANCE_TYPE --days 30
```

### Optimization Examples

#### EC2 Optimization
```bash
# General EC2 optimization
cloudwhisper optimize --service ec2

# Region-specific EC2 optimization
cloudwhisper optimize --service ec2 --region us-west-2 --days 60
```

#### Storage Optimization
```bash
# S3 optimization recommendations
cloudwhisper optimize --service s3

# Find idle resources
cloudwhisper find-idle --days 14
```

#### Database Optimization
```bash
# RDS optimization
cloudwhisper optimize --service rds --region us-east-1
```

## Troubleshooting

### Common Issues

#### 1. AWS Credentials Not Found
**Error:** `Unable to locate credentials`

**Solution:**
```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

#### 2. OpenAI API Key Missing
**Error:** `OpenAI API key is required`

**Solution:**
```bash
export OPENAI_API_KEY=your_openai_api_key
```

#### 3. Insufficient AWS Permissions
**Error:** `AccessDenied` or `UnauthorizedOperation`

**Solution:** Ensure your AWS user/role has the required permissions listed in the Configuration section.

#### 4. Cost Explorer Not Available
**Error:** `Cost Explorer is not available`

**Solution:** Enable Cost Explorer in your AWS account:
1. Go to AWS Billing Console
2. Navigate to Cost Explorer
3. Enable Cost Explorer (may take up to 24 hours)

#### 5. No Cost Data Available
**Error:** `No cost data found`

**Solution:** 
- Ensure you have incurred costs in the specified time period
- Check if Cost Explorer is enabled and has data
- Try a longer time period (e.g., 30 days instead of 7)

### Debug Mode

Enable verbose logging:
```bash
export CLOUDWHISPER_DEBUG=1
cloudwhisper analyze-costs --days 7
```

### Getting Help

1. **Check command help:**
   ```bash
   cloudwhisper --help
   cloudwhisper generate --help
   ```

2. **Check logs:** Look for error messages in the console output

3. **Verify configuration:** Ensure all environment variables are set correctly

4. **Test AWS connectivity:**
   ```bash
   aws sts get-caller-identity
   ```

## Best Practices

### Terraform Code Generation

1. **Be Specific:** Provide detailed descriptions for better code generation
   ```bash
   # Good
   cloudwhisper generate "Create an S3 bucket with versioning enabled, server-side encryption with KMS, and lifecycle policy to transition objects to IA after 30 days"
   
   # Less specific
   cloudwhisper generate "Create S3 bucket"
   ```

2. **Review Generated Code:** Always review and test generated Terraform code before applying

3. **Use Version Control:** Save generated code to version control systems

4. **Customize as Needed:** Generated code is a starting point; customize for your specific needs

### Cost Analysis

1. **Regular Monitoring:** Run cost analysis regularly to track spending trends
   ```bash
   # Weekly analysis
   cloudwhisper analyze-costs --days 7
   
   # Monthly deep dive
   cloudwhisper analyze-costs --days 30 --group-by SERVICE REGION
   ```

2. **Service-Specific Analysis:** Focus on high-cost services
   ```bash
   cloudwhisper analyze-costs --service ec2 --days 30
   ```

3. **Use Appropriate Granularity:** 
   - Use DAILY for short-term analysis (< 30 days)
   - Use MONTHLY for long-term trends (> 30 days)

### Cost Optimization

1. **Act on Recommendations:** Implement optimization recommendations promptly

2. **Monitor After Changes:** Track cost impact after implementing optimizations

3. **Regular Idle Resource Cleanup:**
   ```bash
   # Weekly idle resource check
   cloudwhisper find-idle --days 7
   ```

4. **Consider Savings Plans:** Evaluate Savings Plans for predictable workloads
   ```bash
   cloudwhisper savings-plans
   ```

### Security

1. **Secure Credentials:** Never hardcode AWS credentials or API keys

2. **Use IAM Roles:** Prefer IAM roles over access keys when possible

3. **Least Privilege:** Grant only necessary permissions

4. **Rotate Keys:** Regularly rotate access keys and API keys

### Performance

1. **Use Appropriate Time Ranges:** Longer time ranges take more time to process

2. **Cache Results:** Cost data doesn't change frequently; avoid excessive API calls

3. **Regional Analysis:** Analyze specific regions when possible to reduce data volume

This user guide provides comprehensive information for getting started with CloudWhisper and using it effectively for AWS infrastructure management and cost optimization.
