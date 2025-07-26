#!/usr/bin/env python3

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from decimal import Decimal
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from tabulate import tabulate

console = Console()

class CostAnalyzer:
    """Analyze AWS costs and usage data using Cost Explorer APIs."""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize the cost analyzer with AWS clients."""
        self.region = region
        self.cost_explorer = boto3.client('ce', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        
    def get_cost_and_usage(self, 
                          start_date: datetime.date,
                          end_date: datetime.date,
                          granularity: str = 'DAILY',
                          service_filter: Optional[str] = None,
                          group_by: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get cost and usage data from AWS Cost Explorer."""
        
        try:
            # Build the request parameters
            params = {
                'TimePeriod': {
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                'Granularity': granularity,
                'Metrics': ['BlendedCost', 'UsageQuantity']
            }
            
            # Add service filter if specified
            if service_filter:
                params['Filter'] = {
                    'Dimensions': {
                        'Key': 'SERVICE',
                        'Values': [service_filter.upper()]
                    }
                }
            
            # Add group by dimensions
            if group_by:
                params['GroupBy'] = [{'Type': 'DIMENSION', 'Key': key} for key in group_by]
            
            response = self.cost_explorer.get_cost_and_usage(**params)
            return response
            
        except Exception as e:
            raise Exception(f"Failed to get cost and usage data: {str(e)}")
    
    def get_top_services(self, 
                        start_date: datetime.date,
                        end_date: datetime.date,
                        limit: int = 10) -> List[Dict[str, Any]]:
        """Get top AWS services by cost."""
        
        try:
            response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            
            # Aggregate costs by service
            service_costs = {}
            for result in response['ResultsByTime']:
                for group in result['Groups']:
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    service_costs[service] = service_costs.get(service, 0) + cost
            
            # Sort by cost and return top services
            sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
            return [{'service': service, 'cost': cost} for service, cost in sorted_services[:limit]]
            
        except Exception as e:
            raise Exception(f"Failed to get top services: {str(e)}")
    
    def display_cost_analysis(self, cost_data: Dict[str, Any], service_filter: Optional[str] = None):
        """Display cost analysis results in a formatted table."""
        
        if not cost_data.get('ResultsByTime'):
            console.print("[yellow]No cost data found for the specified period.[/yellow]")
            return
        
        # Create table for cost breakdown
        table = Table(title=f"Cost Analysis{' - ' + service_filter.upper() if service_filter else ''}")
        table.add_column("Date", style="cyan")
        table.add_column("Cost ($)", style="green", justify="right")
        table.add_column("Usage", style="yellow", justify="right")
        
        total_cost = 0
        for result in cost_data['ResultsByTime']:
            date = result['TimePeriod']['Start']
            
            if result.get('Groups'):
                # Grouped data
                for group in result['Groups']:
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    usage = group['Metrics']['UsageQuantity']['Amount']
                    group_key = ' | '.join(group['Keys'])
                    
                    table.add_row(
                        f"{date} ({group_key})",
                        f"{cost:.2f}",
                        f"{float(usage):.2f}"
                    )
                    total_cost += cost
            else:
                # Non-grouped data
                cost = float(result['Total']['BlendedCost']['Amount'])
                usage = result['Total']['UsageQuantity']['Amount']
                
                table.add_row(
                    date,
                    f"{cost:.2f}",
                    f"{float(usage):.2f}"
                )
                total_cost += cost
        
        console.print(table)
        console.print(f"\n[bold]Total Cost: ${total_cost:.2f}[/bold]")
    
    def display_top_services(self, top_services: List[Dict[str, Any]]):
        """Display top services by cost."""
        
        table = Table(title="Top AWS Services by Cost")
        table.add_column("Rank", style="cyan", width=6)
        table.add_column("Service", style="yellow")
        table.add_column("Cost ($)", style="green", justify="right")
        table.add_column("Percentage", style="magenta", justify="right")
        
        total_cost = sum(service['cost'] for service in top_services)
        
        for i, service in enumerate(top_services, 1):
            percentage = (service['cost'] / total_cost * 100) if total_cost > 0 else 0
            table.add_row(
                str(i),
                service['service'],
                f"{service['cost']:.2f}",
                f"{percentage:.1f}%"
            )
        
        console.print(table)

class CostOptimizer:
    """Provide cost optimization recommendations for AWS resources."""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize the cost optimizer with AWS clients."""
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.s3 = boto3.client('s3')
        self.rds = boto3.client('rds', region_name=region)
        self.cost_explorer = boto3.client('ce', region_name='us-east-1')  # CE is only in us-east-1
        self.compute_optimizer = boto3.client('compute-optimizer', region_name='us-east-1')
    
    def analyze_ec2_rightsizing(self, region: Optional[str] = None, days: int = 30) -> List[Dict[str, Any]]:
        """Analyze EC2 instances for rightsizing opportunities."""
        
        recommendations = []
        
        try:
            # Get EC2 instances
            if region:
                ec2_client = boto3.client('ec2', region_name=region)
            else:
                ec2_client = self.ec2
            
            response = ec2_client.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    instance_type = instance['InstanceType']
                    
                    # Get CPU utilization
                    cpu_utilization = self._get_cpu_utilization(instance_id, days)
                    
                    # Analyze for rightsizing
                    recommendation = self._analyze_instance_utilization(
                        instance_id, instance_type, cpu_utilization
                    )
                    
                    if recommendation:
                        recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            console.print(f"[red]Error analyzing EC2 rightsizing:[/red] {str(e)}")
            return []
    
    def analyze_s3_optimization(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Analyze S3 buckets for storage optimization opportunities."""
        
        recommendations = []
        
        try:
            response = self.s3.list_buckets()
            
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                
                # Get bucket location
                try:
                    location = self.s3.get_bucket_location(Bucket=bucket_name)
                    bucket_region = location['LocationConstraint'] or 'us-east-1'
                    
                    if region and bucket_region != region:
                        continue
                        
                except Exception:
                    continue
                
                # Analyze storage classes and lifecycle policies
                recommendation = self._analyze_s3_bucket(bucket_name)
                if recommendation:
                    recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            console.print(f"[red]Error analyzing S3 optimization:[/red] {str(e)}")
            return []
    
    def analyze_rds_optimization(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """Analyze RDS instances for optimization opportunities."""
        
        recommendations = []
        
        try:
            if region:
                rds_client = boto3.client('rds', region_name=region)
            else:
                rds_client = self.rds
            
            response = rds_client.describe_db_instances()
            
            for db_instance in response['DBInstances']:
                db_identifier = db_instance['DBInstanceIdentifier']
                db_class = db_instance['DBInstanceClass']
                engine = db_instance['Engine']
                
                # Analyze RDS utilization
                recommendation = self._analyze_rds_instance(db_identifier, db_class, engine)
                if recommendation:
                    recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            console.print(f"[red]Error analyzing RDS optimization:[/red] {str(e)}")
            return []
    
    def find_idle_resources(self, days: int = 7, region: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Find idle AWS resources that can be terminated."""
        
        idle_resources = {
            'ec2_instances': [],
            'ebs_volumes': [],
            'elastic_ips': [],
            'load_balancers': []
        }
        
        try:
            if region:
                ec2_client = boto3.client('ec2', region_name=region)
                elbv2_client = boto3.client('elbv2', region_name=region)
            else:
                ec2_client = self.ec2
                elbv2_client = boto3.client('elbv2', region_name=self.region)
            
            # Find idle EC2 instances
            idle_resources['ec2_instances'] = self._find_idle_ec2_instances(ec2_client, days)
            
            # Find unattached EBS volumes
            idle_resources['ebs_volumes'] = self._find_unattached_ebs_volumes(ec2_client)
            
            # Find unassociated Elastic IPs
            idle_resources['elastic_ips'] = self._find_unassociated_elastic_ips(ec2_client)
            
            # Find unused load balancers
            idle_resources['load_balancers'] = self._find_unused_load_balancers(elbv2_client)
            
            return idle_resources
            
        except Exception as e:
            console.print(f"[red]Error finding idle resources:[/red] {str(e)}")
            return idle_resources
    
    def get_savings_plans_recommendations(self) -> List[Dict[str, Any]]:
        """Get Savings Plans recommendations from AWS."""
        
        try:
            response = self.cost_explorer.get_savings_plans_purchase_recommendation(
                SavingsPlansType='COMPUTE_SP',
                TermInYears='ONE_YEAR',
                PaymentOption='NO_UPFRONT',
                LookbackPeriodInDays='SIXTY_DAYS'
            )
            
            recommendations = []
            for recommendation in response.get('SavingsPlansRecommendationDetails', []):
                recommendations.append({
                    'hourly_commitment': recommendation.get('HourlyCommitmentToPurchase', '0'),
                    'estimated_savings': recommendation.get('EstimatedMonthlySavings', '0'),
                    'upfront_cost': recommendation.get('UpfrontCost', '0'),
                    'estimated_roi': recommendation.get('EstimatedROI', '0')
                })
            
            return recommendations
            
        except Exception as e:
            console.print(f"[red]Error getting Savings Plans recommendations:[/red] {str(e)}")
            return []
    
    def get_general_recommendations(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get general cost optimization recommendations."""
        
        recommendations = [
            {
                'category': 'Reserved Instances',
                'recommendation': 'Consider purchasing Reserved Instances for consistent workloads',
                'potential_savings': 'Up to 75% compared to On-Demand pricing',
                'action': 'Analyze your usage patterns and purchase RIs for stable workloads'
            },
            {
                'category': 'Spot Instances',
                'recommendation': 'Use Spot Instances for fault-tolerant workloads',
                'potential_savings': 'Up to 90% compared to On-Demand pricing',
                'action': 'Identify workloads that can handle interruptions'
            },
            {
                'category': 'Auto Scaling',
                'recommendation': 'Implement Auto Scaling to match capacity with demand',
                'potential_savings': '10-50% by avoiding over-provisioning',
                'action': 'Set up Auto Scaling Groups with appropriate scaling policies'
            },
            {
                'category': 'Storage Optimization',
                'recommendation': 'Use appropriate S3 storage classes and lifecycle policies',
                'potential_savings': '20-80% on storage costs',
                'action': 'Move infrequently accessed data to cheaper storage classes'
            },
            {
                'category': 'Data Transfer',
                'recommendation': 'Optimize data transfer costs with CloudFront and VPC endpoints',
                'potential_savings': '15-60% on data transfer costs',
                'action': 'Use CloudFront for content delivery and VPC endpoints for AWS services'
            }
        ]
        
        return recommendations
    
    def _get_cpu_utilization(self, instance_id: str, days: int) -> float:
        """Get average CPU utilization for an EC2 instance."""
        
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                avg_cpu = sum(point['Average'] for point in response['Datapoints']) / len(response['Datapoints'])
                return avg_cpu
            
            return 0.0
            
        except Exception:
            return 0.0
    
    def _analyze_instance_utilization(self, instance_id: str, instance_type: str, cpu_utilization: float) -> Optional[Dict[str, Any]]:
        """Analyze instance utilization and provide recommendations."""
        
        if cpu_utilization < 10:
            return {
                'instance_id': instance_id,
                'current_type': instance_type,
                'cpu_utilization': cpu_utilization,
                'recommendation': 'Consider downsizing or terminating',
                'reason': 'Very low CPU utilization',
                'potential_savings': 'High'
            }
        elif cpu_utilization < 25:
            return {
                'instance_id': instance_id,
                'current_type': instance_type,
                'cpu_utilization': cpu_utilization,
                'recommendation': 'Consider downsizing',
                'reason': 'Low CPU utilization',
                'potential_savings': 'Medium'
            }
        elif cpu_utilization > 80:
            return {
                'instance_id': instance_id,
                'current_type': instance_type,
                'cpu_utilization': cpu_utilization,
                'recommendation': 'Consider upsizing',
                'reason': 'High CPU utilization',
                'potential_savings': 'Performance improvement'
            }
        
        return None
    
    def _analyze_s3_bucket(self, bucket_name: str) -> Optional[Dict[str, Any]]:
        """Analyze S3 bucket for optimization opportunities."""
        
        try:
            # Check if lifecycle policy exists
            try:
                self.s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                has_lifecycle = True
            except:
                has_lifecycle = False
            
            if not has_lifecycle:
                return {
                    'bucket_name': bucket_name,
                    'recommendation': 'Implement lifecycle policies',
                    'reason': 'No lifecycle policy found',
                    'potential_savings': 'Medium',
                    'action': 'Set up lifecycle rules to transition objects to cheaper storage classes'
                }
            
            return None
            
        except Exception:
            return None
    
    def _analyze_rds_instance(self, db_identifier: str, db_class: str, engine: str) -> Optional[Dict[str, Any]]:
        """Analyze RDS instance for optimization opportunities."""
        
        # This is a simplified analysis - in practice, you'd check CPU, memory, and I/O metrics
        return {
            'db_identifier': db_identifier,
            'current_class': db_class,
            'engine': engine,
            'recommendation': 'Monitor performance metrics',
            'reason': 'Regular monitoring recommended',
            'potential_savings': 'Variable',
            'action': 'Review CloudWatch metrics for rightsizing opportunities'
        }
    
    def _find_idle_ec2_instances(self, ec2_client, days: int) -> List[Dict[str, Any]]:
        """Find EC2 instances with low utilization."""
        
        idle_instances = []
        
        try:
            response = ec2_client.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    cpu_utilization = self._get_cpu_utilization(instance_id, days)
                    
                    if cpu_utilization < 5:  # Very low utilization
                        idle_instances.append({
                            'instance_id': instance_id,
                            'instance_type': instance['InstanceType'],
                            'cpu_utilization': cpu_utilization,
                            'launch_time': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
                        })
            
            return idle_instances
            
        except Exception:
            return []
    
    def _find_unattached_ebs_volumes(self, ec2_client) -> List[Dict[str, Any]]:
        """Find unattached EBS volumes."""
        
        unattached_volumes = []
        
        try:
            response = ec2_client.describe_volumes(
                Filters=[{'Name': 'status', 'Values': ['available']}]
            )
            
            for volume in response['Volumes']:
                unattached_volumes.append({
                    'volume_id': volume['VolumeId'],
                    'size': volume['Size'],
                    'volume_type': volume['VolumeType'],
                    'create_time': volume['CreateTime'].strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return unattached_volumes
            
        except Exception:
            return []
    
    def _find_unassociated_elastic_ips(self, ec2_client) -> List[Dict[str, Any]]:
        """Find unassociated Elastic IP addresses."""
        
        unassociated_eips = []
        
        try:
            response = ec2_client.describe_addresses()
            
            for address in response['Addresses']:
                if 'InstanceId' not in address and 'NetworkInterfaceId' not in address:
                    unassociated_eips.append({
                        'allocation_id': address.get('AllocationId', 'N/A'),
                        'public_ip': address['PublicIp'],
                        'domain': address['Domain']
                    })
            
            return unassociated_eips
            
        except Exception:
            return []
    
    def _find_unused_load_balancers(self, elbv2_client) -> List[Dict[str, Any]]:
        """Find load balancers with no healthy targets."""
        
        unused_lbs = []
        
        try:
            response = elbv2_client.describe_load_balancers()
            
            for lb in response['LoadBalancers']:
                lb_arn = lb['LoadBalancerArn']
                
                # Get target groups
                tg_response = elbv2_client.describe_target_groups(LoadBalancerArn=lb_arn)
                
                has_healthy_targets = False
                for tg in tg_response['TargetGroups']:
                    health_response = elbv2_client.describe_target_health(
                        TargetGroupArn=tg['TargetGroupArn']
                    )
                    
                    for target in health_response['TargetHealthDescriptions']:
                        if target['TargetHealth']['State'] == 'healthy':
                            has_healthy_targets = True
                            break
                    
                    if has_healthy_targets:
                        break
                
                if not has_healthy_targets:
                    unused_lbs.append({
                        'load_balancer_name': lb['LoadBalancerName'],
                        'load_balancer_arn': lb_arn,
                        'type': lb['Type'],
                        'created_time': lb['CreatedTime'].strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            return unused_lbs
            
        except Exception:
            return []
    
    def display_ec2_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Display EC2 rightsizing recommendations."""
        
        if not recommendations:
            console.print("[green]✓[/green] No EC2 rightsizing opportunities found.")
            return
        
        table = Table(title="EC2 Rightsizing Recommendations")
        table.add_column("Instance ID", style="cyan")
        table.add_column("Current Type", style="yellow")
        table.add_column("CPU Util %", style="red", justify="right")
        table.add_column("Recommendation", style="green")
        table.add_column("Potential Savings", style="magenta")
        
        for rec in recommendations:
            table.add_row(
                rec['instance_id'],
                rec['current_type'],
                f"{rec['cpu_utilization']:.1f}%",
                rec['recommendation'],
                rec['potential_savings']
            )
        
        console.print(table)
    
    def display_s3_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Display S3 optimization recommendations."""
        
        if not recommendations:
            console.print("[green]✓[/green] No S3 optimization opportunities found.")
            return
        
        table = Table(title="S3 Optimization Recommendations")
        table.add_column("Bucket Name", style="cyan")
        table.add_column("Recommendation", style="green")
        table.add_column("Potential Savings", style="magenta")
        table.add_column("Action", style="yellow")
        
        for rec in recommendations:
            table.add_row(
                rec['bucket_name'],
                rec['recommendation'],
                rec['potential_savings'],
                rec['action']
            )
        
        console.print(table)
    
    def display_rds_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Display RDS optimization recommendations."""
        
        if not recommendations:
            console.print("[green]✓[/green] No RDS optimization opportunities found.")
            return
        
        table = Table(title="RDS Optimization Recommendations")
        table.add_column("DB Identifier", style="cyan")
        table.add_column("Current Class", style="yellow")
        table.add_column("Engine", style="blue")
        table.add_column("Recommendation", style="green")
        table.add_column("Action", style="magenta")
        
        for rec in recommendations:
            table.add_row(
                rec['db_identifier'],
                rec['current_class'],
                rec['engine'],
                rec['recommendation'],
                rec['action']
            )
        
        console.print(table)
    
    def display_idle_resources(self, idle_resources: Dict[str, List[Dict[str, Any]]]):
        """Display idle resources that can be terminated."""
        
        total_idle = sum(len(resources) for resources in idle_resources.values())
        
        if total_idle == 0:
            console.print("[green]✓[/green] No idle resources found.")
            return
        
        console.print(f"[yellow]Found {total_idle} idle resources:[/yellow]\n")
        
        # Display idle EC2 instances
        if idle_resources['ec2_instances']:
            table = Table(title="Idle EC2 Instances")
            table.add_column("Instance ID", style="cyan")
            table.add_column("Instance Type", style="yellow")
            table.add_column("CPU Util %", style="red", justify="right")
            table.add_column("Launch Time", style="blue")
            
            for instance in idle_resources['ec2_instances']:
                table.add_row(
                    instance['instance_id'],
                    instance['instance_type'],
                    f"{instance['cpu_utilization']:.1f}%",
                    instance['launch_time']
                )
            
            console.print(table)
            console.print()
        
        # Display unattached EBS volumes
        if idle_resources['ebs_volumes']:
            table = Table(title="Unattached EBS Volumes")
            table.add_column("Volume ID", style="cyan")
            table.add_column("Size (GB)", style="yellow", justify="right")
            table.add_column("Type", style="blue")
            table.add_column("Created", style="green")
            
            for volume in idle_resources['ebs_volumes']:
                table.add_row(
                    volume['volume_id'],
                    str(volume['size']),
                    volume['volume_type'],
                    volume['create_time']
                )
            
            console.print(table)
            console.print()
        
        # Display unassociated Elastic IPs
        if idle_resources['elastic_ips']:
            table = Table(title="Unassociated Elastic IPs")
            table.add_column("Allocation ID", style="cyan")
            table.add_column("Public IP", style="yellow")
            table.add_column("Domain", style="blue")
            
            for eip in idle_resources['elastic_ips']:
                table.add_row(
                    eip['allocation_id'],
                    eip['public_ip'],
                    eip['domain']
                )
            
            console.print(table)
            console.print()
        
        # Display unused load balancers
        if idle_resources['load_balancers']:
            table = Table(title="Unused Load Balancers")
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="yellow")
            table.add_column("Created", style="blue")
            
            for lb in idle_resources['load_balancers']:
                table.add_row(
                    lb['load_balancer_name'],
                    lb['type'],
                    lb['created_time']
                )
            
            console.print(table)
    
    def display_savings_plans_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Display Savings Plans recommendations."""
        
        if not recommendations:
            console.print("[yellow]No Savings Plans recommendations available.[/yellow]")
            return
        
        table = Table(title="Savings Plans Recommendations")
        table.add_column("Hourly Commitment", style="cyan", justify="right")
        table.add_column("Monthly Savings", style="green", justify="right")
        table.add_column("Upfront Cost", style="yellow", justify="right")
        table.add_column("Estimated ROI", style="magenta", justify="right")
        
        for rec in recommendations:
            table.add_row(
                f"${float(rec['hourly_commitment']):.2f}",
                f"${float(rec['estimated_savings']):.2f}",
                f"${float(rec['upfront_cost']):.2f}",
                f"{float(rec['estimated_roi']):.1f}%"
            )
        
        console.print(table)
    
    def display_general_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Display general cost optimization recommendations."""
        
        console.print(Panel.fit("General Cost Optimization Recommendations", style="bold blue"))
        
        for i, rec in enumerate(recommendations, 1):
            console.print(f"\n[bold cyan]{i}. {rec['category']}[/bold cyan]")
            console.print(f"   [green]Recommendation:[/green] {rec['recommendation']}")
            console.print(f"   [yellow]Potential Savings:[/yellow] {rec['potential_savings']}")
            console.print(f"   [blue]Action:[/blue] {rec['action']}")
