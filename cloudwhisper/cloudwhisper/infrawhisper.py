#!/usr/bin/env python3

import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from jinja2 import Template

class TerraformGenerator:
    """Generate Terraform code from natural language descriptions using LLM."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Terraform generator with OpenAI client."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        
        # Terraform templates for common AWS resources
        self.templates = {
            'provider': '''
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "{{ provider_version }}"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
''',
            'variables': '''
variable "{{ name }}" {
  description = "{{ description }}"
  type        = {{ type }}
  {% if default %}default     = {{ default }}{% endif %}
}
''',
            'outputs': '''
output "{{ name }}" {
  description = "{{ description }}"
  value       = {{ value }}
}
'''
        }
    
    def generate_terraform(self, description: str, provider_version: str = "~> 5.0") -> str:
        """Generate Terraform code from natural language description."""
        
        # Create a comprehensive prompt for the LLM
        prompt = self._create_terraform_prompt(description)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Terraform developer specializing in AWS infrastructure. Generate clean, production-ready Terraform code with proper resource naming, tags, and best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            terraform_code = response.choices[0].message.content.strip()
            
            # Add provider configuration
            provider_template = Template(self.templates['provider'])
            provider_config = provider_template.render(provider_version=provider_version)
            
            # Combine provider config with generated code
            full_terraform_code = f"{provider_config}\n{terraform_code}"
            
            return self._clean_terraform_code(full_terraform_code)
            
        except Exception as e:
            raise Exception(f"Failed to generate Terraform code: {str(e)}")
    
    def _create_terraform_prompt(self, description: str) -> str:
        """Create a detailed prompt for Terraform code generation."""
        
        prompt = f"""
Generate Terraform code for the following AWS infrastructure requirement:

"{description}"

Requirements:
1. Use AWS provider version ~> 5.0
2. Include appropriate resource tags (Environment, Project, ManagedBy)
3. Use descriptive resource names with consistent naming convention
4. Include necessary variables for customization
5. Add outputs for important resource attributes
6. Follow Terraform best practices and AWS security guidelines
7. Include comments explaining complex configurations
8. Use data sources where appropriate
9. Ensure resources are properly configured for production use

Please provide only the Terraform resource definitions, variables, and outputs (no provider block as it will be added separately).

Focus on:
- Security best practices
- Cost optimization
- Scalability
- Maintainability

Return only valid Terraform HCL code without any markdown formatting or explanations.
"""
        return prompt
    
    def _clean_terraform_code(self, code: str) -> str:
        """Clean and format the generated Terraform code."""
        
        # Remove markdown code blocks if present
        if "```" in code:
            lines = code.split('\n')
            cleaned_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                if not in_code_block or line.strip() == '':
                    continue
                cleaned_lines.append(line)
            
            code = '\n'.join(cleaned_lines)
        
        # Remove extra whitespace and ensure proper formatting
        lines = [line.rstrip() for line in code.split('\n')]
        
        # Remove empty lines at the beginning and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        
        return '\n'.join(lines)
    
    def validate_terraform_syntax(self, terraform_code: str) -> Dict[str, Any]:
        """Basic validation of Terraform syntax (simplified)."""
        
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Basic checks
        required_blocks = ['resource', 'variable', 'output']
        found_blocks = []
        
        lines = terraform_code.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('resource '):
                found_blocks.append('resource')
            elif line.startswith('variable '):
                found_blocks.append('variable')
            elif line.startswith('output '):
                found_blocks.append('output')
        
        # Check for balanced braces
        open_braces = terraform_code.count('{')
        close_braces = terraform_code.count('}')
        
        if open_braces != close_braces:
            validation_result['valid'] = False
            validation_result['errors'].append(f"Unbalanced braces: {open_braces} opening, {close_braces} closing")
        
        # Check for at least one resource
        if 'resource' not in found_blocks:
            validation_result['warnings'].append("No resources found in generated code")
        
        return validation_result
    
    def generate_terraform_plan_command(self, terraform_dir: str = ".") -> str:
        """Generate the terraform plan command for the generated code."""
        
        commands = [
            f"cd {terraform_dir}",
            "terraform init",
            "terraform validate",
            "terraform plan",
            "# To apply: terraform apply"
        ]
        
        return '\n'.join(commands)
    
    def get_resource_examples(self) -> Dict[str, str]:
        """Get examples of common AWS resources that can be generated."""
        
        examples = {
            "S3 Bucket": "Create an S3 bucket with versioning and encryption enabled",
            "VPC": "Create a VPC with public and private subnets across 2 availability zones",
            "EC2 Instance": "Launch a t3.micro EC2 instance with security group allowing SSH",
            "RDS Database": "Create a MySQL RDS instance with backup retention",
            "Lambda Function": "Create a Python Lambda function with IAM role",
            "API Gateway": "Set up REST API Gateway with Lambda integration",
            "CloudFront": "Create CloudFront distribution for S3 static website",
            "ECS Cluster": "Set up ECS cluster with Fargate service",
            "Load Balancer": "Create Application Load Balancer with target groups",
            "Auto Scaling": "Set up Auto Scaling Group with launch template"
        }
        
        return examples
