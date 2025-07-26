#!/usr/bin/env python3
"""
CloudWhisper Usage Examples

This script demonstrates how to use CloudWhisper programmatically.
"""

import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import cloudwhisper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloudwhisper.infrawhisper import TerraformGenerator
from cloudwhisper.cloudfuel import CostAnalyzer, CostOptimizer

def example_terraform_generation():
    """Example of generating Terraform code."""
    print("=== Terraform Generation Example ===")
    
    # Initialize the generator (requires OPENAI_API_KEY environment variable)
    try:
        generator = TerraformGenerator()
        
        # Generate Terraform code for an S3 bucket
        description = "Create an S3 bucket with versioning enabled and server-side encryption"
        terraform_code = generator.generate_terraform(description)
        
        print("Generated Terraform code:")
        print(terraform_code)
        
        # Validate the generated code
        validation = generator.validate_terraform_syntax(terraform_code)
        print(f"\nValidation result: {'Valid' if validation['valid'] else 'Invalid'}")
        if validation['errors']:
            print("Errors:", validation['errors'])
        if validation['warnings']:
            print("Warnings:", validation['warnings'])
            
    except Exception as e:
        print(f"Error: {e}")

def example_cost_analysis():
    """Example of analyzing AWS costs."""
    print("\n=== Cost Analysis Example ===")
    
    try:
        analyzer = CostAnalyzer()
        
        # Analyze costs for the last 7 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        cost_data = analyzer.get_cost_and_usage(
            start_date=start_date,
            end_date=end_date,
            granularity='DAILY'
        )
        
        analyzer.display_cost_analysis(cost_data)
        
        # Get top services
        top_services = analyzer.get_top_services(start_date, end_date, limit=5)
        analyzer.display_top_services(top_services)
        
    except Exception as e:
        print(f"Error: {e}")

def example_cost_optimization():
    """Example of getting cost optimization recommendations."""
    print("\n=== Cost Optimization Example ===")
    
    try:
        optimizer = CostOptimizer()
        
        # Analyze EC2 rightsizing opportunities
        ec2_recommendations = optimizer.analyze_ec2_rightsizing(days=30)
        optimizer.display_ec2_recommendations(ec2_recommendations)
        
        # Find idle resources
        idle_resources = optimizer.find_idle_resources(days=7)
        optimizer.display_idle_resources(idle_resources)
        
        # Get general recommendations
        general_recommendations = optimizer.get_general_recommendations(days=30)
        optimizer.display_general_recommendations(general_recommendations)
        
    except Exception as e:
        print(f"Error: {e}")

def example_s3_optimization():
    """Example of S3 optimization analysis."""
    print("\n=== S3 Optimization Example ===")
    
    try:
        optimizer = CostOptimizer()
        
        # Analyze S3 buckets for optimization
        s3_recommendations = optimizer.analyze_s3_optimization()
        optimizer.display_s3_recommendations(s3_recommendations)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("CloudWhisper Usage Examples")
    print("=" * 50)
    
    # Check for required environment variables
    if not os.getenv('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY not set. Terraform generation will fail.")
    
    if not os.getenv('AWS_ACCESS_KEY_ID'):
        print("Warning: AWS credentials not set. Cost analysis will fail.")
    
    print()
    
    # Run examples
    example_terraform_generation()
    example_cost_analysis()
    example_cost_optimization()
    example_s3_optimization()
    
    print("\n=== Examples Complete ===")
    print("To use CloudWhisper CLI, run: cloudwhisper --help")
