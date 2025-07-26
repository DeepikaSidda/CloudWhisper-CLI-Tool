# CloudWhisper Documentation

Welcome to the CloudWhisper documentation! This comprehensive guide will help you get started with CloudWhisper, an AI-powered CLI tool for AWS infrastructure management and cost optimization.

## 📚 Documentation Overview

### Quick Start
- **[Installation Guide](INSTALLATION.md)** - Complete installation instructions for all platforms
- **[User Guide](USER_GUIDE.md)** - Comprehensive user manual with all features
- **[Examples & Tutorials](EXAMPLES.md)** - Practical examples and step-by-step tutorials

### Reference
- **[API Reference](API_REFERENCE.md)** - Complete API documentation for programmatic usage
- **[Troubleshooting](TROUBLESHOOTING.md)** - Solutions to common issues and problems

### Additional Resources
- **[Project Summary](../PROJECT_SUMMARY.md)** - Technical overview and architecture
- **[Configuration Examples](../config.example.yaml)** - Sample configuration file
- **[Usage Examples](../examples/)** - Code examples and demonstrations

## 🚀 Quick Start

### 1. Installation
```bash
git clone <repository-url>
cd cloudwhisper
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 2. Configuration
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
export OPENAI_API_KEY=your_openai_key
```

### 3. Basic Usage
```bash
# Generate Terraform code
cloudwhisper generate "Create an S3 bucket with versioning"

# Analyze costs
cloudwhisper analyze-costs --days 30

# Get optimization recommendations
cloudwhisper optimize

# Find idle resources
cloudwhisper find-idle --days 7
```

## 🎯 Key Features

### 🤖 AI-Powered Terraform Generation
- Convert natural language to production-ready Terraform code
- Support for all major AWS services
- Best practices and security compliance built-in
- Syntax validation and error checking

### 💰 Comprehensive Cost Analysis
- Multi-dimensional cost breakdowns
- Service-level analysis and trends
- Time-series cost visualization
- Top services identification

### 🔧 Intelligent Optimization
- EC2 rightsizing recommendations
- S3 storage optimization
- RDS performance tuning
- Idle resource detection
- Savings Plans recommendations

### 📊 Rich Console Output
- Colorized tables and charts
- Progress indicators
- Interactive panels
- Formatted displays

## 📖 Documentation Structure

```
docs/
├── README.md              # This file - documentation overview
├── INSTALLATION.md        # Complete installation guide
├── USER_GUIDE.md         # Comprehensive user manual
├── API_REFERENCE.md      # API documentation
├── EXAMPLES.md           # Examples and tutorials
└── TROUBLESHOOTING.md    # Problem solving guide
```

## 🛠 Core Modules

### InfraWhisper
Handles AI-powered Terraform code generation using OpenAI GPT-4.

**Key Classes:**
- `TerraformGenerator` - Main code generation class

**Features:**
- Natural language to Terraform conversion
- Syntax validation
- Best practices enforcement
- Template system

### CloudFuel
Provides AWS cost analysis and optimization recommendations.

**Key Classes:**
- `CostAnalyzer` - Cost analysis and reporting
- `CostOptimizer` - Optimization recommendations

**Features:**
- Cost Explorer integration
- Multi-dimensional analysis
- Resource optimization
- Idle resource detection

## 🔧 Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `generate` | Generate Terraform code | `cloudwhisper generate "Create VPC"` |
| `analyze-costs` | Analyze AWS costs | `cloudwhisper analyze-costs --days 30` |
| `optimize` | Get optimization recommendations | `cloudwhisper optimize --service ec2` |
| `find-idle` | Find idle resources | `cloudwhisper find-idle --days 7` |
| `savings-plans` | Get Savings Plans recommendations | `cloudwhisper savings-plans` |

## 🔐 Security & Permissions

### Required AWS Permissions
CloudWhisper requires specific AWS IAM permissions for cost analysis and resource optimization. See the [Installation Guide](INSTALLATION.md#aws-permissions) for the complete permissions policy.

### API Keys
- **OpenAI API Key**: Required for Terraform generation
- **AWS Credentials**: Required for cost analysis and optimization

### Best Practices
- Use IAM roles when possible
- Follow least privilege principle
- Rotate API keys regularly
- Never commit credentials to version control

## 🚨 Common Issues

| Issue | Quick Solution | Documentation |
|-------|----------------|---------------|
| Command not found | Activate virtual environment | [Troubleshooting](TROUBLESHOOTING.md#issue-command-not-found) |
| AWS credentials missing | Run `aws configure` | [Installation](INSTALLATION.md#aws-configuration) |
| OpenAI API key missing | Set `OPENAI_API_KEY` | [User Guide](USER_GUIDE.md#configuration) |
| Cost Explorer not enabled | Enable in AWS Console | [Troubleshooting](TROUBLESHOOTING.md#issue-cost-explorer-not-enabled) |

## 📝 Examples

### Generate Infrastructure
```bash
# S3 bucket with features
cloudwhisper generate "Create S3 bucket with versioning, encryption, and lifecycle policy"

# VPC with subnets
cloudwhisper generate "Create VPC with public and private subnets across 2 AZs"

# Auto Scaling Group
cloudwhisper generate "Create Auto Scaling Group with launch template and scaling policies"
```

### Cost Analysis
```bash
# Basic analysis
cloudwhisper analyze-costs --days 30

# Service-specific
cloudwhisper analyze-costs --service ec2 --days 14

# Multi-dimensional
cloudwhisper analyze-costs --group-by SERVICE REGION --days 30
```

### Optimization
```bash
# General recommendations
cloudwhisper optimize

# EC2 rightsizing
cloudwhisper optimize --service ec2 --region us-east-1

# Find idle resources
cloudwhisper find-idle --days 7
```

## 🔄 Integration

### CI/CD Pipelines
CloudWhisper can be integrated into CI/CD pipelines for:
- Automated cost reporting
- Infrastructure code generation
- Cost threshold monitoring
- Optimization recommendations

See [Examples](EXAMPLES.md#integration-examples) for GitHub Actions and Jenkins examples.

### Monitoring Systems
Integration with monitoring systems for:
- Cost alerts
- Performance tracking
- Automated reporting
- Dashboard integration

## 🆘 Getting Help

### Documentation
1. Check the relevant documentation section
2. Review examples and tutorials
3. Consult the troubleshooting guide

### Self-Help
1. Enable debug mode: `export CLOUDWHISPER_DEBUG=1`
2. Check system requirements
3. Verify configuration
4. Test with minimal examples

### Community Support
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides and examples
- **Stack Overflow**: Tag questions with `cloudwhisper`

### Creating Issues
When creating GitHub issues, include:
- Operating system and Python version
- Complete error messages
- Steps to reproduce
- Debug output (sanitized)
- CloudWhisper version

## 🔄 Updates and Maintenance

### Staying Updated
```bash
# Update from source
git pull origin main
pip install -e .

# Update from PyPI (when available)
pip install --upgrade cloudwhisper
```

### Version Information
```bash
# Check current version
cloudwhisper --version

# Check installed packages
pip show cloudwhisper
```

## 📄 License and Contributing

CloudWhisper is open source software. See the main repository for:
- License information
- Contributing guidelines
- Code of conduct
- Development setup

## 🎯 Next Steps

1. **Start with Installation**: Follow the [Installation Guide](INSTALLATION.md)
2. **Learn the Basics**: Read the [User Guide](USER_GUIDE.md)
3. **Try Examples**: Work through [Examples & Tutorials](EXAMPLES.md)
4. **Explore API**: Check the [API Reference](API_REFERENCE.md)
5. **Get Help**: Use the [Troubleshooting Guide](TROUBLESHOOTING.md) when needed

Happy cloud optimizing with CloudWhisper! 🚀
