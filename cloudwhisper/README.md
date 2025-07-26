# CloudWhisper

CloudWhisper is an AI-powered CLI tool that helps you manage AWS infrastructure and optimize cloud costs through natural language interactions.

<p align="center">
  <img src="/cloudwhisper/cloudwhisper.jpg" alt="CloudWhisper" width="600"/>
</p>


## Features

- **InfraWhisper**: Generate Terraform code from natural language descriptions
- **CloudFuel**: Analyze AWS costs and get optimization recommendations
- **Cost Analysis**: Deep dive into your AWS spending patterns
- **Resource Optimization**: Get actionable recommendations to reduce costs

## Installation

```bash
pip install -e .
```
## Configuration

Set your AWS credentials and OpenAI API key:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
export OPENAI_API_KEY=your_openai_key
```

## Usage

### Generate Terraform Code
```bash
cloudwhisper generate "Create an S3 bucket with versioning enabled"
cloudwhisper generate "Set up a VPC with public and private subnets"
```

### Analyze Costs
```bash
cloudwhisper analyze-costs --days 30
cloudwhisper analyze-costs --service ec2 --days 7
```

### Get Optimization Recommendations
```bash
cloudwhisper optimize
cloudwhisper optimize --service ec2
```


## Requirements

- Python 3.8+
- AWS CLI configured
- OpenAI API key (for Terraform generation)
