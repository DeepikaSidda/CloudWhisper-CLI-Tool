#!/usr/bin/env python3
"""
Generate CloudWhisper Architecture Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 16)
ax.set_ylim(0, 12)
ax.axis('off')

# Colors
primary_blue = '#2E86AB'
secondary_blue = '#A23B72'
accent_orange = '#F18F01'
light_gray = '#F5F5F5'
dark_gray = '#333333'
green = '#4CAF50'
red = '#F44336'

# Title
ax.text(8, 11.5, 'CloudWhisper Architecture & Workflow', 
        fontsize=24, fontweight='bold', ha='center', color=dark_gray)

# Subtitle
ax.text(8, 11, 'AI-Powered AWS Infrastructure Management & Cost Optimization CLI Tool', 
        fontsize=14, ha='center', color=secondary_blue, style='italic')

# Main Components Section
ax.text(2, 10.2, 'Core Modules', fontsize=16, fontweight='bold', color=dark_gray)

# InfraWhisper Module
infrawhisper_box = FancyBboxPatch((0.5, 8.5), 3, 1.5, 
                                  boxstyle="round,pad=0.1", 
                                  facecolor=primary_blue, 
                                  edgecolor=dark_gray, 
                                  alpha=0.8)
ax.add_patch(infrawhisper_box)
ax.text(2, 9.5, 'InfraWhisper', fontsize=14, fontweight='bold', 
        ha='center', va='center', color='white')
ax.text(2, 9.1, 'Terraform Code Generation', fontsize=10, 
        ha='center', va='center', color='white')
ax.text(2, 8.8, '• Natural Language → IaC', fontsize=8, 
        ha='center', va='center', color='white')

# CloudFuel Module
cloudfuel_box = FancyBboxPatch((4.5, 8.5), 3, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=accent_orange, 
                               edgecolor=dark_gray, 
                               alpha=0.8)
ax.add_patch(cloudfuel_box)
ax.text(6, 9.5, 'CloudFuel', fontsize=14, fontweight='bold', 
        ha='center', va='center', color='white')
ax.text(6, 9.1, 'Cost Analysis & Optimization', fontsize=10, 
        ha='center', va='center', color='white')
ax.text(6, 8.8, '• Cost Explorer Integration', fontsize=8, 
        ha='center', va='center', color='white')

# CLI Interface
cli_box = FancyBboxPatch((8.5, 8.5), 3, 1.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=secondary_blue, 
                         edgecolor=dark_gray, 
                         alpha=0.8)
ax.add_patch(cli_box)
ax.text(10, 9.5, 'CLI Interface', fontsize=14, fontweight='bold', 
        ha='center', va='center', color='white')
ax.text(10, 9.1, 'Command Line Tool', fontsize=10, 
        ha='center', va='center', color='white')
ax.text(10, 8.8, '• Click Framework', fontsize=8, 
        ha='center', va='center', color='white')

# External APIs Section
ax.text(13, 10.2, 'External APIs', fontsize=16, fontweight='bold', color=dark_gray)

# OpenAI API
openai_box = FancyBboxPatch((12, 8.5), 2.5, 0.7, 
                            boxstyle="round,pad=0.05", 
                            facecolor=green, 
                            edgecolor=dark_gray, 
                            alpha=0.8)
ax.add_patch(openai_box)
ax.text(13.25, 8.85, 'OpenAI GPT-4', fontsize=10, fontweight='bold', 
        ha='center', va='center', color='white')

# AWS APIs
aws_box = FancyBboxPatch((12, 7.5), 2.5, 0.7, 
                         boxstyle="round,pad=0.05", 
                         facecolor='#FF9900', 
                         edgecolor=dark_gray, 
                         alpha=0.8)
ax.add_patch(aws_box)
ax.text(13.25, 7.85, 'AWS APIs', fontsize=10, fontweight='bold', 
        ha='center', va='center', color='white')

# Commands Section
ax.text(1, 7.5, 'Available Commands', fontsize=16, fontweight='bold', color=dark_gray)

commands = [
    ('generate', 'Generate Terraform code from natural language', primary_blue),
    ('analyze-costs', 'Analyze AWS costs and usage patterns', accent_orange),
    ('optimize', 'Get cost optimization recommendations', green),
    ('find-idle', 'Find idle resources to terminate', red),
    ('savings-plans', 'Get Savings Plans recommendations', secondary_blue)
]

y_pos = 6.8
for cmd, desc, color in commands:
    cmd_box = FancyBboxPatch((0.5, y_pos-0.15), 2, 0.3, 
                             boxstyle="round,pad=0.02", 
                             facecolor=color, 
                             edgecolor=dark_gray, 
                             alpha=0.8)
    ax.add_patch(cmd_box)
    ax.text(1.5, y_pos, cmd, fontsize=10, fontweight='bold', 
            ha='center', va='center', color='white')
    ax.text(3, y_pos, desc, fontsize=9, 
            ha='left', va='center', color=dark_gray)
    y_pos -= 0.5

# Workflow Section
ax.text(8, 7.5, 'Workflow', fontsize=16, fontweight='bold', color=dark_gray)

# Workflow boxes
workflow_steps = [
    ('User Input', 'Natural language or CLI commands'),
    ('Processing', 'AI analysis or AWS API calls'),
    ('Output', 'Terraform code or cost reports')
]

x_positions = [8, 10, 12]
for i, (title, desc) in enumerate(workflow_steps):
    workflow_box = FancyBboxPatch((x_positions[i]-0.7, 6.5), 1.4, 0.8, 
                                  boxstyle="round,pad=0.05", 
                                  facecolor=light_gray, 
                                  edgecolor=dark_gray, 
                                  alpha=0.9)
    ax.add_patch(workflow_box)
    ax.text(x_positions[i], 7, title, fontsize=10, fontweight='bold', 
            ha='center', va='center', color=dark_gray)
    ax.text(x_positions[i], 6.7, desc, fontsize=8, 
            ha='center', va='center', color=dark_gray)
    
    # Add arrows between workflow steps
    if i < len(workflow_steps) - 1:
        arrow = patches.FancyArrowPatch((x_positions[i]+0.7, 6.9), 
                                        (x_positions[i+1]-0.7, 6.9),
                                        arrowstyle='->', 
                                        mutation_scale=20, 
                                        color=dark_gray)
        ax.add_patch(arrow)

# Features Section
ax.text(1, 5.5, 'Key Features', fontsize=16, fontweight='bold', color=dark_gray)

features = [
    '🤖 AI-powered Terraform generation using OpenAI GPT-4',
    '💰 Comprehensive AWS cost analysis with Cost Explorer',
    '🔧 Intelligent optimization recommendations',
    '🔍 Idle resource detection and cleanup suggestions',
    '💡 Savings Plans and Reserved Instance recommendations',
    '📊 Rich console output with tables and visualizations',
    '🛡️ Security best practices and compliance checks',
    '⚡ High-performance API integration with rate limiting'
]

y_pos = 5
for i, feature in enumerate(features):
    if i < 4:
        x_pos = 0.5
        y_current = y_pos - (i * 0.3)
    else:
        x_pos = 8.5
        y_current = y_pos - ((i-4) * 0.3)
    
    ax.text(x_pos, y_current, feature, fontsize=10, 
            ha='left', va='center', color=dark_gray)

# Technical Stack Section
ax.text(1, 3.5, 'Technical Stack', fontsize=16, fontweight='bold', color=dark_gray)

tech_stack = [
    ('Python 3.8+', primary_blue),
    ('Click Framework', accent_orange),
    ('Boto3 SDK', '#FF9900'),
    ('OpenAI API', green),
    ('Rich Console', secondary_blue),
    ('Jinja2 Templates', red)
]

x_pos = 1
for tech, color in tech_stack:
    tech_box = FancyBboxPatch((x_pos-0.3, 2.8), len(tech)*0.12, 0.4, 
                              boxstyle="round,pad=0.02", 
                              facecolor=color, 
                              edgecolor=dark_gray, 
                              alpha=0.8)
    ax.add_patch(tech_box)
    ax.text(x_pos, 3, tech, fontsize=9, fontweight='bold', 
            ha='left', va='center', color='white')
    x_pos += len(tech)*0.12 + 0.8

# Use Cases Section
ax.text(8.5, 3.5, 'Use Cases', fontsize=16, fontweight='bold', color=dark_gray)

use_cases = [
    '• Infrastructure as Code generation',
    '• Cloud cost monitoring and alerts',
    '• Resource optimization and rightsizing',
    '• Automated cost reporting',
    '• CI/CD pipeline integration',
    '• Multi-account cost analysis'
]

y_pos = 3.1
for use_case in use_cases:
    ax.text(8.5, y_pos, use_case, fontsize=10, 
            ha='left', va='center', color=dark_gray)
    y_pos -= 0.25

# Installation Section
ax.text(1, 2.2, 'Installation', fontsize=16, fontweight='bold', color=dark_gray)

install_box = FancyBboxPatch((1, 1.2), 6, 0.8, 
                             boxstyle="round,pad=0.05", 
                             facecolor=light_gray, 
                             edgecolor=dark_gray, 
                             alpha=0.9)
ax.add_patch(install_box)

install_text = """pip install -e .
export AWS_ACCESS_KEY_ID=your_key
export OPENAI_API_KEY=your_key
cloudwhisper --help"""

ax.text(1.2, 1.6, install_text, fontsize=9, fontfamily='monospace',
        ha='left', va='center', color=dark_gray)

# Example Usage Section
ax.text(8.5, 2.2, 'Example Usage', fontsize=16, fontweight='bold', color=dark_gray)

usage_box = FancyBboxPatch((8.5, 1.2), 6.5, 0.8, 
                           boxstyle="round,pad=0.05", 
                           facecolor=light_gray, 
                           edgecolor=dark_gray, 
                           alpha=0.9)
ax.add_patch(usage_box)

usage_text = """cloudwhisper generate "Create S3 bucket with versioning"
cloudwhisper analyze-costs --days 30
cloudwhisper optimize --service ec2
cloudwhisper find-idle --days 7"""

ax.text(8.7, 1.6, usage_text, fontsize=9, fontfamily='monospace',
        ha='left', va='center', color=dark_gray)

# Footer
ax.text(8, 0.5, 'CloudWhisper - Simplifying AWS Infrastructure Management with AI', 
        fontsize=12, ha='center', color=secondary_blue, style='italic')

# Add connection lines
# InfraWhisper to OpenAI
conn1 = ConnectionPatch((3.5, 9.2), (12, 8.85), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc=green, alpha=0.6)
ax.add_artist(conn1)

# CloudFuel to AWS
conn2 = ConnectionPatch((7.5, 9.2), (12, 7.85), "data", "data",
                        arrowstyle="->", shrinkA=5, shrinkB=5, 
                        mutation_scale=20, fc='#FF9900', alpha=0.6)
ax.add_artist(conn2)

plt.tight_layout()
plt.savefig('/mnt/c/Users/sidda/OneDrive/Desktop/Q-Developer-Challenge/cloudwhisper/cloudwhisper_architecture.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("CloudWhisper architecture diagram saved as 'cloudwhisper_architecture.png'")
