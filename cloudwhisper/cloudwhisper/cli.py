#!/usr/bin/env python3

import click
import os
import sys
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .infrawhisper import TerraformGenerator
from .cloudfuel import CostAnalyzer, CostOptimizer

console = Console()

@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    CloudWhisper - AI-powered AWS infrastructure and cost optimization CLI tool
    
    Generate Terraform code from natural language and optimize your AWS costs.
    """
    pass

@main.command()
@click.argument('description')
@click.option('--output', '-o', help='Output file for generated Terraform code')
@click.option('--provider-version', default='~> 5.0', help='AWS provider version')
def generate(description, output, provider_version):
    """Generate Terraform code from natural language description."""
    try:
        console.print(f"[bold blue]Generating Terraform code for:[/bold blue] {description}")
        
        generator = TerraformGenerator()
        terraform_code = generator.generate_terraform(description, provider_version)
        
        if output:
            with open(output, 'w') as f:
                f.write(terraform_code)
            console.print(f"[green]✓[/green] Terraform code saved to {output}")
        else:
            console.print("\n[bold yellow]Generated Terraform Code:[/bold yellow]")
            console.print(Panel(terraform_code, title="Terraform Configuration", border_style="green"))
            
    except Exception as e:
        console.print(f"[red]Error generating Terraform code:[/red] {str(e)}")
        sys.exit(1)

@main.command()
@click.option('--days', '-d', default=30, help='Number of days to analyze (default: 30)')
@click.option('--service', '-s', help='Specific AWS service to analyze')
@click.option('--granularity', default='DAILY', type=click.Choice(['DAILY', 'MONTHLY']), 
              help='Cost data granularity')
@click.option('--group-by', multiple=True, 
              type=click.Choice(['SERVICE', 'REGION', 'INSTANCE_TYPE', 'USAGE_TYPE']),
              help='Group costs by dimension')
def analyze_costs(days, service, granularity, group_by):
    """Analyze AWS costs and usage data."""
    try:
        console.print(f"[bold blue]Analyzing AWS costs for the last {days} days...[/bold blue]")
        
        analyzer = CostAnalyzer()
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Get cost data
        cost_data = analyzer.get_cost_and_usage(
            start_date=start_date,
            end_date=end_date,
            granularity=granularity,
            service_filter=service,
            group_by=list(group_by) if group_by else None
        )
        
        # Display results
        analyzer.display_cost_analysis(cost_data, service)
        
        # Get top services if no specific service requested
        if not service:
            top_services = analyzer.get_top_services(start_date, end_date, limit=10)
            analyzer.display_top_services(top_services)
            
    except Exception as e:
        console.print(f"[red]Error analyzing costs:[/red] {str(e)}")
        sys.exit(1)

@main.command()
@click.option('--service', '-s', help='Specific AWS service to optimize')
@click.option('--region', '-r', help='Specific AWS region to analyze')
@click.option('--days', '-d', default=30, help='Days of data to analyze for recommendations')
def optimize(service, region, days):
    """Get cost optimization recommendations."""
    try:
        console.print("[bold blue]Analyzing your AWS resources for optimization opportunities...[/bold blue]")
        
        optimizer = CostOptimizer()
        
        # Get recommendations based on service
        if service == 'ec2' or not service:
            console.print("\n[yellow]Analyzing EC2 instances...[/yellow]")
            ec2_recommendations = optimizer.analyze_ec2_rightsizing(region, days)
            optimizer.display_ec2_recommendations(ec2_recommendations)
        
        if service == 's3' or not service:
            console.print("\n[yellow]Analyzing S3 storage...[/yellow]")
            s3_recommendations = optimizer.analyze_s3_optimization(region)
            optimizer.display_s3_recommendations(s3_recommendations)
        
        if service == 'rds' or not service:
            console.print("\n[yellow]Analyzing RDS instances...[/yellow]")
            rds_recommendations = optimizer.analyze_rds_optimization(region)
            optimizer.display_rds_recommendations(rds_recommendations)
        
        # General recommendations
        console.print("\n[yellow]General optimization recommendations...[/yellow]")
        general_recommendations = optimizer.get_general_recommendations(days)
        optimizer.display_general_recommendations(general_recommendations)
        
    except Exception as e:
        console.print(f"[red]Error getting optimization recommendations:[/red] {str(e)}")
        sys.exit(1)

@main.command()
@click.option('--days', '-d', default=7, help='Number of days to look back for idle resources')
@click.option('--region', '-r', help='Specific AWS region to analyze')
def find_idle(days, region):
    """Find idle AWS resources that can be terminated to save costs."""
    try:
        console.print(f"[bold blue]Searching for idle resources in the last {days} days...[/bold blue]")
        
        optimizer = CostOptimizer()
        idle_resources = optimizer.find_idle_resources(days, region)
        optimizer.display_idle_resources(idle_resources)
        
    except Exception as e:
        console.print(f"[red]Error finding idle resources:[/red] {str(e)}")
        sys.exit(1)

@main.command()
def savings_plans():
    """Get Savings Plans recommendations."""
    try:
        console.print("[bold blue]Analyzing Savings Plans opportunities...[/bold blue]")
        
        optimizer = CostOptimizer()
        recommendations = optimizer.get_savings_plans_recommendations()
        optimizer.display_savings_plans_recommendations(recommendations)
        
    except Exception as e:
        console.print(f"[red]Error getting Savings Plans recommendations:[/red] {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
