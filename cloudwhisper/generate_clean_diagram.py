#!/usr/bin/env python3
"""
Generate Clean CloudWhisper Architecture Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Rectangle
import numpy as np

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(18, 14))
ax.set_xlim(0, 18)
ax.set_ylim(0, 14)
ax.axis('off')

# Colors
primary_blue = '#2E86AB'
secondary_blue = '#A23B72'
accent_orange = '#F18F01'
light_gray = '#F5F5F5'
dark_gray = '#333333'
green = '#4CAF50'
red = '#F44336'
aws_orange = '#FF9900'

# Title
ax.text(9, 13.5, 'CloudWhisper', 
        fontsize=32, fontweight='bold', ha='center', color=primary_blue)
ax.text(9, 13, 'AI-Powered AWS Infrastructure Management & Cost Optimization CLI Tool', 
        fontsize=16, ha='center', color=secondary_blue, style='italic')

# Main Architecture Section
ax.text(9, 12.2, 'System Architecture', fontsize=20, fontweight='bold', ha='center', color=dark_gray)

# User Layer
user_box = FancyBboxPatch((1, 10.5), 16, 1, 
                          boxstyle="round,pad=0.1", 
                          facecolor=light_gray, 
                          edgecolor=dark_gray, 
                          linewidth=2)
ax.add_patch(user_box)
ax.text(9, 11, 'USER INTERFACE', fontsize=14, fontweight='bold', 
        ha='center', va='center', color=dark_gray)
ax.text(3, 10.7, 'Command Line Interface (CLI)', fontsize=12, 
        ha='left', va='center', color=dark_gray)
ax.text(15, 10.7, 'Rich Console Output', fontsize=12, 
        ha='right', va='center', color=dark_gray)

# Core Modules Layer
modules_y = 8.5

# InfraWhisper Module
infrawhisper_box = FancyBboxPatch((1, modules_y), 5, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=primary_blue, 
                                  edgecolor=dark_gray, 
                                  linewidth=2,
                                  alpha=0.9)
ax.add_patch(infrawhisper_box)
ax.text(3.5, modules_y+1, 'INFRAWHISPER MODULE', fontsize=14, fontweight='bold', 
        ha='center', va='center', color='white')
ax.text(3.5, modules_y+0.6, 'Terraform Code Generation', fontsize=11, 
        ha='center', va='center', color='white')
ax.text(3.5, modules_y+0.3, '• Natural Language Processing', fontsize=9, 
        ha='center', va='center', color='white')
ax.text(3.5, modules_y+0.1, '• Infrastructure as Code', fontsize=9, 
        ha='center', va='center', color='white')

# CloudFuel Module
cloudfuel_box = FancyBboxPatch((6.5, modules_y), 5, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=accent_orange, 
                               edgecolor=dark_gray, 
                               linewidth=2,
                               alpha=0.9)
ax.add_patch(cloudfuel_box)
ax.text(9, modules_y+1, 'CLOUDFUEL MODULE', fontsize=14, fontweight='bold', 
        ha='center', va='center', color='white')
ax.text(9, modules_y+0.6, 'Cost Analysis & Optimization', fontsize=11, 
        ha='center', va='center', color='white')
ax.text(9, modules_y+0.3, '• Cost Explorer Integration', fontsize=9, 
        ha='center', va='center', color='white')
ax.text(9, modules_y+0.1, '• Resource Optimization', fontsize=9, 
        ha='center', va='center', color='white')

# CLI Controller Module
cli_box = FancyBboxPatch((12, modules_y), 5, 1.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=secondary_blue, 
                         edgecolor=dark_gray, 
                         linewidth=2,
                         alpha=0.9)
ax.add_patch(cli_box)
ax.text(14.5, modules_y+1, 'CLI CONTROLLER', fontsize=14, fontweight='bold', 
        ha='center', va='center', color='white')
ax.text(14.5, modules_y+0.6, 'Command Processing', fontsize=11, 
        ha='center', va='center', color='white')
ax.text(14.5, modules_y+0.3, '• Click Framework', fontsize=9, 
        ha='center', va='center', color='white')
ax.text(14.5, modules_y+0.1, '• Error Handling', fontsize=9, 
        ha='center', va='center', color='white')

# External APIs Layer
api_y = 6.5
ax.text(9, api_y+1.2, 'External API Integration', fontsize=16, fontweight='bold', ha='center', color=dark_gray)

# OpenAI API
openai_box = FancyBboxPatch((2, api_y), 4, 0.8, 
                            boxstyle="round,pad=0.05", 
                            facecolor=green, 
                            edgecolor=dark_gray, 
                            linewidth=2,
                            alpha=0.9)
ax.add_patch(openai_box)
ax.text(4, api_y+0.4, 'OpenAI GPT-4 API', fontsize=12, fontweight='bold', 
        ha='center', va='center', color='white')

# AWS APIs
aws_box = FancyBboxPatch((12, api_y), 4, 0.8, 
                         boxstyle="round,pad=0.05", 
                         facecolor=aws_orange, 
                         edgecolor=dark_gray, 
                         linewidth=2,
                         alpha=0.9)
ax.add_patch(aws_box)
ax.text(14, api_y+0.4, 'AWS APIs', fontsize=12, fontweight='bold', 
        ha='center', va='center', color='white')

# AWS Services details
aws_services = ['Cost Explorer', 'EC2', 'S3', 'RDS', 'CloudWatch']
ax.text(14, api_y+0.1, ' • '.join(aws_services), fontsize=9, 
        ha='center', va='center', color='white')

# Commands Section
commands_y = 4.5
ax.text(2, commands_y+0.8, 'Available Commands', fontsize=16, fontweight='bold', color=dark_gray)

commands = [
    ('generate', 'Generate Terraform code from natural language', primary_blue),
    ('analyze-costs', 'Analyze AWS costs and usage patterns', accent_orange),
    ('optimize', 'Get cost optimization recommendations', green),
    ('find-idle', 'Find idle resources to terminate', red),
    ('savings-plans', 'Get Savings Plans recommendations', secondary_blue)
]

y_pos = commands_y + 0.4
for cmd, desc, color in commands:
    cmd_box = FancyBboxPatch((1, y_pos-0.15), 2.5, 0.3, 
                             boxstyle="round,pad=0.02", 
                             facecolor=color, 
                             edgecolor=dark_gray, 
                             alpha=0.9)
    ax.add_patch(cmd_box)
    ax.text(2.25, y_pos, cmd, fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white')
    ax.text(4, y_pos, desc, fontsize=10, 
            ha='left', va='center', color=dark_gray)
    y_pos -= 0.4

# Features Section
features_y = 4.5
ax.text(10, features_y+0.8, 'Key Features', fontsize=16, fontweight='bold', color=dark_gray)

features = [
    'AI-powered Terraform generation using OpenAI GPT-4',
    'Comprehensive AWS cost analysis with Cost Explorer',
    'Intelligent optimization recommendations',
    'Idle resource detection and cleanup suggestions',
    'Savings Plans and Reserved Instance recommendations',
    'Rich console output with tables and visualizations',
    'Security best practices and compliance checks',
    'High-performance API integration with rate limiting'
]

y_pos = features_y + 0.4
for feature in features:
    ax.text(10, y_pos, f'• {feature}', fontsize=10, 
            ha='left', va='center', color=dark_gray)
    y_pos -= 0.3

# Installation & Usage Section
install_y = 1.5
ax.text(2, install_y+0.8, 'Quick Start', fontsize=16, fontweight='bold', color=dark_gray)

install_box = FancyBboxPatch((1, install_y-0.3), 7, 1, 
                             boxstyle="round,pad=0.05", 
                             facecolor=light_gray, 
                             edgecolor=dark_gray, 
                             alpha=0.9)
ax.add_patch(install_box)

install_text = """1. pip install -e .
2. export AWS_ACCESS_KEY_ID=your_key
3. export OPENAI_API_KEY=your_key
4. cloudwhisper --help"""

ax.text(1.2, install_y+0.1, install_text, fontsize=10, fontfamily='monospace',
        ha='left', va='center', color=dark_gray)

# Example Usage
ax.text(10, install_y+0.8, 'Example Commands', fontsize=16, fontweight='bold', color=dark_gray)

usage_box = FancyBboxPatch((9, install_y-0.3), 8, 1, 
                           boxstyle="round,pad=0.05", 
                           facecolor=light_gray, 
                           edgecolor=dark_gray, 
                           alpha=0.9)
ax.add_patch(usage_box)

usage_text = """cloudwhisper generate "Create S3 bucket with versioning"
cloudwhisper analyze-costs --days 30 --service ec2
cloudwhisper optimize --service ec2 --region us-east-1
cloudwhisper find-idle --days 7"""

ax.text(9.2, install_y+0.1, usage_text, fontsize=10, fontfamily='monospace',
        ha='left', va='center', color=dark_gray)

# Add connection arrows
# User to CLI Controller
arrow1 = patches.FancyArrowPatch((9, 10.5), (14.5, 9.5),
                                arrowstyle='->', mutation_scale=20, 
                                color=dark_gray, alpha=0.7, linewidth=2)
ax.add_patch(arrow1)

# CLI Controller to modules
arrow2 = patches.FancyArrowPatch((12, 9.2), (6, 9.2),
                                arrowstyle='->', mutation_scale=20, 
                                color=dark_gray, alpha=0.7, linewidth=2)
ax.add_patch(arrow2)

# InfraWhisper to OpenAI
arrow3 = patches.FancyArrowPatch((3.5, 8.5), (4, 7.3),
                                arrowstyle='->', mutation_scale=20, 
                                color=green, alpha=0.8, linewidth=2)
ax.add_patch(arrow3)

# CloudFuel to AWS
arrow4 = patches.FancyArrowPatch((9, 8.5), (14, 7.3),
                                arrowstyle='->', mutation_scale=20, 
                                color=aws_orange, alpha=0.8, linewidth=2)
ax.add_patch(arrow4)

# Add labels for arrows
ax.text(11, 9.4, 'Command\nRouting', fontsize=9, ha='center', va='center', 
        color=dark_gray, bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

ax.text(2.5, 7.8, 'AI\nGeneration', fontsize=9, ha='center', va='center', 
        color=green, bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

ax.text(11.5, 7.8, 'Cost\nAnalysis', fontsize=9, ha='center', va='center', 
        color=aws_orange, bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('/mnt/c/Users/sidda/OneDrive/Desktop/Q-Developer-Challenge/cloudwhisper/cloudwhisper_clean_architecture.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("Clean CloudWhisper architecture diagram saved as 'cloudwhisper_clean_architecture.png'")
