# CloudWhisper API Reference

## Table of Contents
1. [Module Overview](#module-overview)
2. [InfraWhisper Module](#infrawhisper-module)
3. [CloudFuel Module](#cloudfuel-module)
4. [CLI Module](#cli-module)
5. [Error Handling](#error-handling)
6. [Configuration](#configuration)

## Module Overview

CloudWhisper consists of three main modules:

- **`infrawhisper`**: Terraform code generation using AI
- **`cloudfuel`**: AWS cost analysis and optimization
- **`cli`**: Command-line interface

## InfraWhisper Module

### TerraformGenerator Class

The `TerraformGenerator` class handles AI-powered Terraform code generation.

#### Constructor

```python
TerraformGenerator(api_key: Optional[str] = None)
```

**Parameters:**
- `api_key` (str, optional): OpenAI API key. If not provided, reads from `OPENAI_API_KEY` environment variable.

**Raises:**
- `ValueError`: If OpenAI API key is not provided or found in environment variables.

**Example:**
```python
from cloudwhisper.infrawhisper import TerraformGenerator

# Using environment variable
generator = TerraformGenerator()

# Using explicit API key
generator = TerraformGenerator(api_key="your-api-key")
```

#### Methods

##### `generate_terraform(description: str, provider_version: str = "~> 5.0") -> str`

Generate Terraform code from natural language description.

**Parameters:**
- `description` (str): Natural language description of the infrastructure to create
- `provider_version` (str, optional): AWS provider version constraint. Default: "~> 5.0"

**Returns:**
- `str`: Generated Terraform code

**Raises:**
- `Exception`: If code generation fails

**Example:**
```python
generator = TerraformGenerator()
code = generator.generate_terraform(
    "Create an S3 bucket with versioning enabled",
    provider_version="~> 5.0"
)
print(code)
```

##### `validate_terraform_syntax(terraform_code: str) -> Dict[str, Any]`

Validate basic Terraform syntax.

**Parameters:**
- `terraform_code` (str): Terraform code to validate

**Returns:**
- `Dict[str, Any]`: Validation result with keys:
  - `valid` (bool): Whether the syntax is valid
  - `errors` (List[str]): List of syntax errors
  - `warnings` (List[str]): List of warnings

**Example:**
```python
generator = TerraformGenerator()
result = generator.validate_terraform_syntax(terraform_code)
if result['valid']:
    print("Syntax is valid")
else:
    print("Errors:", result['errors'])
```

##### `generate_terraform_plan_command(terraform_dir: str = ".") -> str`

Generate terraform plan command for the generated code.

**Parameters:**
- `terraform_dir` (str, optional): Directory containing Terraform files. Default: "."

**Returns:**
- `str`: Multi-line string with terraform commands

**Example:**
```python
generator = TerraformGenerator()
commands = generator.generate_terraform_plan_command("/path/to/terraform")
print(commands)
```

##### `get_resource_examples() -> Dict[str, str]`

Get examples of common AWS resources that can be generated.

**Returns:**
- `Dict[str, str]`: Dictionary mapping resource types to example descriptions

**Example:**
```python
generator = TerraformGenerator()
examples = generator.get_resource_examples()
for resource_type, description in examples.items():
    print(f"{resource_type}: {description}")
```

## CloudFuel Module

### CostAnalyzer Class

The `CostAnalyzer` class handles AWS cost analysis using Cost Explorer APIs.

#### Constructor

```python
CostAnalyzer(region: str = 'us-east-1')
```

**Parameters:**
- `region` (str, optional): AWS region for clients. Default: 'us-east-1'

**Example:**
```python
from cloudwhisper.cloudfuel import CostAnalyzer

analyzer = CostAnalyzer(region='us-west-2')
```

#### Methods

##### `get_cost_and_usage(start_date, end_date, granularity='DAILY', service_filter=None, group_by=None) -> Dict[str, Any]`

Get cost and usage data from AWS Cost Explorer.

**Parameters:**
- `start_date` (datetime.date): Start date for cost analysis
- `end_date` (datetime.date): End date for cost analysis
- `granularity` (str, optional): 'DAILY' or 'MONTHLY'. Default: 'DAILY'
- `service_filter` (str, optional): Filter by specific AWS service
- `group_by` (List[str], optional): Group by dimensions (SERVICE, REGION, etc.)

**Returns:**
- `Dict[str, Any]`: Cost Explorer API response

**Raises:**
- `Exception`: If API call fails

**Example:**
```python
from datetime import datetime, timedelta

analyzer = CostAnalyzer()
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

cost_data = analyzer.get_cost_and_usage(
    start_date=start_date,
    end_date=end_date,
    granularity='DAILY',
    service_filter='ec2',
    group_by=['REGION']
)
```

##### `get_top_services(start_date, end_date, limit=10) -> List[Dict[str, Any]]`

Get top AWS services by cost.

**Parameters:**
- `start_date` (datetime.date): Start date for analysis
- `end_date` (datetime.date): End date for analysis
- `limit` (int, optional): Number of top services to return. Default: 10

**Returns:**
- `List[Dict[str, Any]]`: List of services with cost information

**Example:**
```python
top_services = analyzer.get_top_services(start_date, end_date, limit=5)
for service in top_services:
    print(f"{service['service']}: ${service['cost']:.2f}")
```

##### `display_cost_analysis(cost_data, service_filter=None)`

Display cost analysis results in formatted tables.

**Parameters:**
- `cost_data` (Dict[str, Any]): Cost data from `get_cost_and_usage()`
- `service_filter` (str, optional): Service filter used in the query

**Example:**
```python
analyzer.display_cost_analysis(cost_data, service_filter='ec2')
```

##### `display_top_services(top_services)`

Display top services in a formatted table.

**Parameters:**
- `top_services` (List[Dict[str, Any]]): Top services from `get_top_services()`

**Example:**
```python
analyzer.display_top_services(top_services)
```

### CostOptimizer Class

The `CostOptimizer` class provides cost optimization recommendations.

#### Constructor

```python
CostOptimizer(region: str = 'us-east-1')
```

**Parameters:**
- `region` (str, optional): AWS region for clients. Default: 'us-east-1'

**Example:**
```python
from cloudwhisper.cloudfuel import CostOptimizer

optimizer = CostOptimizer(region='us-west-2')
```

#### Methods

##### `analyze_ec2_rightsizing(region=None, days=30) -> List[Dict[str, Any]]`

Analyze EC2 instances for rightsizing opportunities.

**Parameters:**
- `region` (str, optional): Specific region to analyze
- `days` (int, optional): Days of metrics to analyze. Default: 30

**Returns:**
- `List[Dict[str, Any]]`: List of rightsizing recommendations

**Example:**
```python
optimizer = CostOptimizer()
recommendations = optimizer.analyze_ec2_rightsizing(region='us-east-1', days=30)
for rec in recommendations:
    print(f"Instance {rec['instance_id']}: {rec['recommendation']}")
```

##### `analyze_s3_optimization(region=None) -> List[Dict[str, Any]]`

Analyze S3 buckets for storage optimization opportunities.

**Parameters:**
- `region` (str, optional): Specific region to analyze

**Returns:**
- `List[Dict[str, Any]]`: List of S3 optimization recommendations

**Example:**
```python
s3_recommendations = optimizer.analyze_s3_optimization()
for rec in s3_recommendations:
    print(f"Bucket {rec['bucket_name']}: {rec['recommendation']}")
```

##### `analyze_rds_optimization(region=None) -> List[Dict[str, Any]]`

Analyze RDS instances for optimization opportunities.

**Parameters:**
- `region` (str, optional): Specific region to analyze

**Returns:**
- `List[Dict[str, Any]]`: List of RDS optimization recommendations

**Example:**
```python
rds_recommendations = optimizer.analyze_rds_optimization()
for rec in rds_recommendations:
    print(f"DB {rec['db_identifier']}: {rec['recommendation']}")
```

##### `find_idle_resources(days=7, region=None) -> Dict[str, List[Dict[str, Any]]]`

Find idle AWS resources that can be terminated.

**Parameters:**
- `days` (int, optional): Days to look back for idle detection. Default: 7
- `region` (str, optional): Specific region to analyze

**Returns:**
- `Dict[str, List[Dict[str, Any]]]`: Dictionary with resource types as keys and lists of idle resources as values

**Example:**
```python
idle_resources = optimizer.find_idle_resources(days=14)
for resource_type, resources in idle_resources.items():
    print(f"Found {len(resources)} idle {resource_type}")
```

##### `get_savings_plans_recommendations() -> List[Dict[str, Any]]`

Get Savings Plans recommendations from AWS.

**Returns:**
- `List[Dict[str, Any]]`: List of Savings Plans recommendations

**Example:**
```python
savings_recommendations = optimizer.get_savings_plans_recommendations()
for rec in savings_recommendations:
    print(f"Hourly commitment: ${rec['hourly_commitment']}")
```

##### `get_general_recommendations(days=30) -> List[Dict[str, Any]]`

Get general cost optimization recommendations.

**Parameters:**
- `days` (int, optional): Days of data to consider. Default: 30

**Returns:**
- `List[Dict[str, Any]]`: List of general recommendations

**Example:**
```python
general_recs = optimizer.get_general_recommendations()
for rec in general_recs:
    print(f"{rec['category']}: {rec['recommendation']}")
```

#### Display Methods

The `CostOptimizer` class includes several display methods for formatted output:

- `display_ec2_recommendations(recommendations)`
- `display_s3_recommendations(recommendations)`
- `display_rds_recommendations(recommendations)`
- `display_idle_resources(idle_resources)`
- `display_savings_plans_recommendations(recommendations)`
- `display_general_recommendations(recommendations)`

## CLI Module

### Main Function

```python
main()
```

Entry point for the CLI application. Handles command parsing and execution.

### Command Functions

#### `generate(description, output, provider_version)`

CLI command for Terraform code generation.

**Parameters:**
- `description` (str): Natural language description
- `output` (str, optional): Output file path
- `provider_version` (str, optional): AWS provider version

#### `analyze_costs(days, service, granularity, group_by)`

CLI command for cost analysis.

**Parameters:**
- `days` (int): Number of days to analyze
- `service` (str, optional): Specific service to analyze
- `granularity` (str): Cost data granularity
- `group_by` (tuple): Dimensions to group by

#### `optimize(service, region, days)`

CLI command for optimization recommendations.

**Parameters:**
- `service` (str, optional): Specific service to optimize
- `region` (str, optional): Specific region to analyze
- `days` (int): Days of data to analyze

#### `find_idle(days, region)`

CLI command for finding idle resources.

**Parameters:**
- `days` (int): Days to look back
- `region` (str, optional): Specific region to analyze

#### `savings_plans()`

CLI command for Savings Plans recommendations.

## Error Handling

### Common Exceptions

#### `ValueError`
Raised when invalid parameters are provided, such as missing API keys.

#### `Exception`
Generic exception for API failures, network issues, or other runtime errors.

### Error Response Format

Most methods that can fail will raise exceptions with descriptive error messages:

```python
try:
    generator = TerraformGenerator()
    code = generator.generate_terraform("Create S3 bucket")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Generation failed: {e}")
```

### AWS API Errors

AWS API errors are typically wrapped in generic exceptions with the original error message:

```python
try:
    analyzer = CostAnalyzer()
    cost_data = analyzer.get_cost_and_usage(start_date, end_date)
except Exception as e:
    if "AccessDenied" in str(e):
        print("Insufficient AWS permissions")
    elif "InvalidParameterValue" in str(e):
        print("Invalid parameter provided to AWS API")
    else:
        print(f"AWS API error: {e}")
```

## Configuration

### Environment Variables

The following environment variables are used:

- `OPENAI_API_KEY`: OpenAI API key for Terraform generation
- `AWS_ACCESS_KEY_ID`: AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: AWS secret access key
- `AWS_DEFAULT_REGION`: Default AWS region
- `CLOUDWHISPER_DEBUG`: Enable debug logging (set to "1")

### Configuration File

Optional configuration file at `~/.cloudwhisper/config.yaml`:

```yaml
aws:
  default_region: us-east-1
  profile: default

openai:
  api_key: your_key_here
  model: gpt-4
  temperature: 0.1
  max_tokens: 2000

cost_analysis:
  default_days: 30
  default_granularity: DAILY
  currency: USD

optimization:
  cpu_threshold_low: 10
  cpu_threshold_high: 80
  idle_days_threshold: 7

terraform:
  default_provider_version: "~> 5.0"
  include_tags: true
  default_tags:
    Environment: dev
    ManagedBy: CloudWhisper
```

### AWS Profiles

CloudWhisper respects AWS CLI profiles. You can specify a profile using:

```bash
export AWS_PROFILE=my-profile
cloudwhisper analyze-costs
```

## Usage Examples

### Programmatic Usage

```python
from cloudwhisper import TerraformGenerator, CostAnalyzer, CostOptimizer
from datetime import datetime, timedelta

# Generate Terraform code
generator = TerraformGenerator()
terraform_code = generator.generate_terraform(
    "Create an S3 bucket with versioning and encryption"
)
print(terraform_code)

# Analyze costs
analyzer = CostAnalyzer()
end_date = datetime.now().date()
start_date = end_date - timedelta(days=30)

cost_data = analyzer.get_cost_and_usage(start_date, end_date)
analyzer.display_cost_analysis(cost_data)

# Get optimization recommendations
optimizer = CostOptimizer()
ec2_recs = optimizer.analyze_ec2_rightsizing()
optimizer.display_ec2_recommendations(ec2_recs)
```

### CLI Usage

```bash
# Generate Terraform code
cloudwhisper generate "Create VPC with subnets" -o vpc.tf

# Analyze costs
cloudwhisper analyze-costs --days 30 --service ec2

# Get optimization recommendations
cloudwhisper optimize --service ec2 --region us-east-1

# Find idle resources
cloudwhisper find-idle --days 7
```

This API reference provides comprehensive information about all classes, methods, and functions available in CloudWhisper for programmatic usage.
