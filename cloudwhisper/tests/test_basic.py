#!/usr/bin/env python3
"""
Basic tests for CloudWhisper CLI tool
"""

import pytest
import os
from unittest.mock import patch, MagicMock

# Import the modules to test
from cloudwhisper.infrawhisper import TerraformGenerator
from cloudwhisper.cloudfuel import CostAnalyzer, CostOptimizer

class TestTerraformGenerator:
    """Test the TerraformGenerator class."""
    
    def test_init_without_api_key(self):
        """Test initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                TerraformGenerator()
    
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            generator = TerraformGenerator()
            assert generator.api_key == 'test-key'
    
    def test_clean_terraform_code(self):
        """Test cleaning of Terraform code."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            generator = TerraformGenerator()
            
            # Test removing markdown code blocks
            code_with_markdown = '''```hcl
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}
```'''
            
            cleaned = generator._clean_terraform_code(code_with_markdown)
            assert '```' not in cleaned
            assert 'resource "aws_s3_bucket" "example"' in cleaned
    
    def test_validate_terraform_syntax(self):
        """Test basic Terraform syntax validation."""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            generator = TerraformGenerator()
            
            # Test valid syntax
            valid_code = '''
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}
'''
            result = generator.validate_terraform_syntax(valid_code)
            assert result['valid'] is True
            assert len(result['errors']) == 0
            
            # Test invalid syntax (unbalanced braces)
            invalid_code = '''
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
'''
            result = generator.validate_terraform_syntax(invalid_code)
            assert result['valid'] is False
            assert len(result['errors']) > 0

class TestCostAnalyzer:
    """Test the CostAnalyzer class."""
    
    @patch('boto3.client')
    def test_init(self, mock_boto_client):
        """Test CostAnalyzer initialization."""
        analyzer = CostAnalyzer()
        assert analyzer.region == 'us-east-1'
        # Verify boto3 clients were created
        assert mock_boto_client.call_count >= 2  # ce and cloudwatch clients

class TestCostOptimizer:
    """Test the CostOptimizer class."""
    
    @patch('boto3.client')
    def test_init(self, mock_boto_client):
        """Test CostOptimizer initialization."""
        optimizer = CostOptimizer()
        assert optimizer.region == 'us-east-1'
        # Verify boto3 clients were created
        assert mock_boto_client.call_count >= 5  # Multiple AWS service clients
    
    def test_analyze_instance_utilization(self):
        """Test instance utilization analysis."""
        with patch('boto3.client'):
            optimizer = CostOptimizer()
            
            # Test very low utilization
            result = optimizer._analyze_instance_utilization('i-123', 't3.micro', 5.0)
            assert result is not None
            assert result['recommendation'] == 'Consider downsizing or terminating'
            assert result['potential_savings'] == 'High'
            
            # Test low utilization
            result = optimizer._analyze_instance_utilization('i-123', 't3.micro', 20.0)
            assert result is not None
            assert result['recommendation'] == 'Consider downsizing'
            assert result['potential_savings'] == 'Medium'
            
            # Test high utilization
            result = optimizer._analyze_instance_utilization('i-123', 't3.micro', 85.0)
            assert result is not None
            assert result['recommendation'] == 'Consider upsizing'
            
            # Test normal utilization
            result = optimizer._analyze_instance_utilization('i-123', 't3.micro', 50.0)
            assert result is None

if __name__ == '__main__':
    pytest.main([__file__])
