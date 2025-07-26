#!/usr/bin/env python3
"""
Generate CloudWhisper Workflow Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, ConnectionPatch
import numpy as np

# Set up the figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 20))

# Colors
primary_blue = '#2E86AB'
secondary_blue = '#A23B72'
accent_orange = '#F18F01'
light_gray = '#F5F5F5'
dark_gray = '#333333'
green = '#4CAF50'
red = '#F44336'
aws_orange = '#FF9900'

# ============ TOP DIAGRAM: TERRAFORM GENERATION WORKFLOW ============
ax1.set_xlim(0, 16)
ax1.set_ylim(0, 12)
ax1.axis('off')

# Title
ax1.text(8, 11.5, 'CloudWhisper Terraform Generation Workflow', 
         fontsize=20, fontweight='bold', ha='center', color=primary_blue)

# Step 1: User Input
step1_box = FancyBboxPatch((1, 9.5), 3, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=light_gray, 
                           edgecolor=dark_gray, 
                           linewidth=2)
ax1.add_patch(step1_box)
ax1.text(2.5, 10.5, 'STEP 1', fontsize=12, fontweight='bold', 
         ha='center', va='center', color=dark_gray)
ax1.text(2.5, 10.1, 'User Input', fontsize=11, 
         ha='center', va='center', color=dark_gray)
ax1.text(2.5, 9.8, 'Natural Language', fontsize=9, 
         ha='center', va='center', color=dark_gray)

# Example input
example_box1 = FancyBboxPatch((0.5, 8.5), 4, 0.8, 
                              boxstyle="round,pad=0.05", 
                              facecolor='#E8F4FD', 
                              edgecolor=primary_blue, 
                              alpha=0.8)
ax1.add_patch(example_box1)
ax1.text(2.5, 8.9, 'Example:', fontsize=10, fontweight='bold', 
         ha='center', va='center', color=primary_blue)
ax1.text(2.5, 8.6, '"Create S3 bucket with versioning"', fontsize=9, 
         ha='center', va='center', color=dark_gray, style='italic')

# Step 2: CLI Processing
step2_box = FancyBboxPatch((6, 9.5), 3, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=secondary_blue, 
                           edgecolor=dark_gray, 
                           linewidth=2,
                           alpha=0.9)
ax1.add_patch(step2_box)
ax1.text(7.5, 10.5, 'STEP 2', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax1.text(7.5, 10.1, 'CLI Processing', fontsize=11, 
         ha='center', va='center', color='white')
ax1.text(7.5, 9.8, 'Command Parsing', fontsize=9, 
         ha='center', va='center', color='white')

# Step 3: OpenAI API
step3_box = FancyBboxPatch((11, 9.5), 3, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=green, 
                           edgecolor=dark_gray, 
                           linewidth=2,
                           alpha=0.9)
ax1.add_patch(step3_box)
ax1.text(12.5, 10.5, 'STEP 3', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax1.text(12.5, 10.1, 'OpenAI GPT-4', fontsize=11, 
         ha='center', va='center', color='white')
ax1.text(12.5, 9.8, 'AI Generation', fontsize=9, 
         ha='center', va='center', color='white')

# Step 4: Code Generation
step4_box = FancyBboxPatch((6, 6.5), 3, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=accent_orange, 
                           edgecolor=dark_gray, 
                           linewidth=2,
                           alpha=0.9)
ax1.add_patch(step4_box)
ax1.text(7.5, 7.5, 'STEP 4', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax1.text(7.5, 7.1, 'Code Generation', fontsize=11, 
         ha='center', va='center', color='white')
ax1.text(7.5, 6.8, 'Terraform HCL', fontsize=9, 
         ha='center', va='center', color='white')

# Step 5: Validation & Output
step5_box = FancyBboxPatch((1, 6.5), 3, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=primary_blue, 
                           edgecolor=dark_gray, 
                           linewidth=2,
                           alpha=0.9)
ax1.add_patch(step5_box)
ax1.text(2.5, 7.5, 'STEP 5', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax1.text(2.5, 7.1, 'Validation', fontsize=11, 
         ha='center', va='center', color='white')
ax1.text(2.5, 6.8, '& Output', fontsize=9, 
         ha='center', va='center', color='white')

# Final Output
output_box = FancyBboxPatch((11, 6.5), 3, 1.5, 
                            boxstyle="round,pad=0.1", 
                            facecolor='#2E7D32', 
                            edgecolor=dark_gray, 
                            linewidth=2,
                            alpha=0.9)
ax1.add_patch(output_box)
ax1.text(12.5, 7.5, 'OUTPUT', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax1.text(12.5, 7.1, 'Terraform Code', fontsize=11, 
         ha='center', va='center', color='white')
ax1.text(12.5, 6.8, 'Ready to Deploy', fontsize=9, 
         ha='center', va='center', color='white')

# Example output
example_box2 = FancyBboxPatch((10.5, 4.5), 4, 1.5, 
                              boxstyle="round,pad=0.05", 
                              facecolor='#E8F5E8', 
                              edgecolor=green, 
                              alpha=0.8)
ax1.add_patch(example_box2)
ax1.text(12.5, 5.6, 'Generated Code:', fontsize=10, fontweight='bold', 
         ha='center', va='center', color=green)
terraform_code = '''resource "aws_s3_bucket" "example" {
  bucket = "my-bucket"
}'''
ax1.text(12.5, 5, terraform_code, fontsize=8, fontfamily='monospace',
         ha='center', va='center', color=dark_gray)

# Add arrows for workflow
arrows = [
    ((4, 10.2), (6, 10.2)),  # Step 1 to 2
    ((9, 10.2), (11, 10.2)), # Step 2 to 3
    ((12.5, 9.5), (7.5, 8)),  # Step 3 to 4
    ((6, 7.2), (4, 7.2)),     # Step 4 to 5
    ((2.5, 6.5), (12.5, 6.5)) # Step 5 to Output (curved)
]

for start, end in arrows:
    arrow = patches.FancyArrowPatch(start, end,
                                   arrowstyle='->', mutation_scale=20, 
                                   color=dark_gray, alpha=0.7, linewidth=2)
    ax1.add_patch(arrow)

# Add process details
details_y = 3.5
ax1.text(8, details_y, 'Process Details', fontsize=16, fontweight='bold', ha='center', color=dark_gray)

details = [
    '1. User provides natural language description via CLI',
    '2. CLI parses command and validates input parameters',
    '3. OpenAI GPT-4 processes description with Terraform context',
    '4. AI generates production-ready Terraform HCL code',
    '5. System validates syntax and applies best practices',
    '6. Clean, deployable Terraform code is output to console or file'
]

y_pos = details_y - 0.3
for detail in details:
    ax1.text(1, y_pos, detail, fontsize=10, 
             ha='left', va='center', color=dark_gray)
    y_pos -= 0.3

# ============ BOTTOM DIAGRAM: COST ANALYSIS WORKFLOW ============
ax2.set_xlim(0, 16)
ax2.set_ylim(0, 12)
ax2.axis('off')

# Title
ax2.text(8, 11.5, 'CloudWhisper Cost Analysis & Optimization Workflow', 
         fontsize=20, fontweight='bold', ha='center', color=accent_orange)

# Step 1: User Command
step1_box = FancyBboxPatch((1, 9.5), 2.5, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=light_gray, 
                           edgecolor=dark_gray, 
                           linewidth=2)
ax2.add_patch(step1_box)
ax2.text(2.25, 10.5, 'STEP 1', fontsize=12, fontweight='bold', 
         ha='center', va='center', color=dark_gray)
ax2.text(2.25, 10.1, 'Cost Analysis', fontsize=10, 
         ha='center', va='center', color=dark_gray)
ax2.text(2.25, 9.8, 'Command', fontsize=10, 
         ha='center', va='center', color=dark_gray)

# Step 2: AWS Cost Explorer
step2_box = FancyBboxPatch((4.5, 9.5), 2.5, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=aws_orange, 
                           edgecolor=dark_gray, 
                           linewidth=2,
                           alpha=0.9)
ax2.add_patch(step2_box)
ax2.text(5.75, 10.5, 'STEP 2', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax2.text(5.75, 10.1, 'Cost Explorer', fontsize=10, 
         ha='center', va='center', color='white')
ax2.text(5.75, 9.8, 'API Calls', fontsize=10, 
         ha='center', va='center', color='white')

# Step 3: Data Processing
step3_box = FancyBboxPatch((8, 9.5), 2.5, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=secondary_blue, 
                           edgecolor=dark_gray, 
                           linewidth=2,
                           alpha=0.9)
ax2.add_patch(step3_box)
ax2.text(9.25, 10.5, 'STEP 3', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax2.text(9.25, 10.1, 'Data Analysis', fontsize=10, 
         ha='center', va='center', color='white')
ax2.text(9.25, 9.8, '& Processing', fontsize=10, 
         ha='center', va='center', color='white')

# Step 4: CloudWatch Metrics
step4_box = FancyBboxPatch((11.5, 9.5), 2.5, 1.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=green, 
                           edgecolor=dark_gray, 
                           linewidth=2,
                           alpha=0.9)
ax2.add_patch(step4_box)
ax2.text(12.75, 10.5, 'STEP 4', fontsize=12, fontweight='bold', 
         ha='center', va='center', color='white')
ax2.text(12.75, 10.1, 'CloudWatch', fontsize=10, 
         ha='center', va='center', color='white')
ax2.text(12.75, 9.8, 'Metrics', fontsize=10, 
         ha='center', va='center', color='white')

# Analysis Types
analysis_y = 7.5
ax2.text(8, analysis_y+0.8, 'Analysis Types', fontsize=16, fontweight='bold', ha='center', color=dark_gray)

# Cost Analysis
cost_box = FancyBboxPatch((1, analysis_y-0.5), 3, 1, 
                          boxstyle="round,pad=0.05", 
                          facecolor='#FFF3E0', 
                          edgecolor=accent_orange, 
                          alpha=0.8)
ax2.add_patch(cost_box)
ax2.text(2.5, analysis_y, 'Cost Analysis', fontsize=11, fontweight='bold', 
         ha='center', va='center', color=accent_orange)
ax2.text(2.5, analysis_y-0.3, '• Service breakdown\n• Time trends\n• Regional costs', fontsize=9, 
         ha='center', va='center', color=dark_gray)

# Optimization
opt_box = FancyBboxPatch((4.5, analysis_y-0.5), 3, 1, 
                         boxstyle="round,pad=0.05", 
                         facecolor='#E8F5E8', 
                         edgecolor=green, 
                         alpha=0.8)
ax2.add_patch(opt_box)
ax2.text(6, analysis_y, 'Optimization', fontsize=11, fontweight='bold', 
         ha='center', va='center', color=green)
ax2.text(6, analysis_y-0.3, '• EC2 rightsizing\n• S3 lifecycle\n• Idle resources', fontsize=9, 
         ha='center', va='center', color=dark_gray)

# Recommendations
rec_box = FancyBboxPatch((8, analysis_y-0.5), 3, 1, 
                         boxstyle="round,pad=0.05", 
                         facecolor='#F3E5F5', 
                         edgecolor=secondary_blue, 
                         alpha=0.8)
ax2.add_patch(rec_box)
ax2.text(9.5, analysis_y, 'Recommendations', fontsize=11, fontweight='bold', 
         ha='center', va='center', color=secondary_blue)
ax2.text(9.5, analysis_y-0.3, '• Savings Plans\n• Reserved Instances\n• Best practices', fontsize=9, 
         ha='center', va='center', color=dark_gray)

# Reporting
report_box = FancyBboxPatch((11.5, analysis_y-0.5), 3, 1, 
                            boxstyle="round,pad=0.05", 
                            facecolor='#FFEBEE', 
                            edgecolor=red, 
                            alpha=0.8)
ax2.add_patch(report_box)
ax2.text(13, analysis_y, 'Reporting', fontsize=11, fontweight='bold', 
         ha='center', va='center', color=red)
ax2.text(13, analysis_y-0.3, '• Rich tables\n• Visualizations\n• Export options', fontsize=9, 
         ha='center', va='center', color=dark_gray)

# Output Examples
output_y = 5
ax2.text(8, output_y+0.8, 'Output Examples', fontsize=16, fontweight='bold', ha='center', color=dark_gray)

# Cost table example
table_box = FancyBboxPatch((1, output_y-1), 6, 1.5, 
                           boxstyle="round,pad=0.05", 
                           facecolor=light_gray, 
                           edgecolor=dark_gray, 
                           alpha=0.9)
ax2.add_patch(table_box)
ax2.text(4, output_y+0.2, 'Cost Analysis Table', fontsize=11, fontweight='bold', 
         ha='center', va='center', color=dark_gray)
table_text = '''Service    | Cost ($) | Change
EC2        | 1,234.56 | +12%
S3         |   456.78 | -5%
RDS        |   789.01 | +8%'''
ax2.text(4, output_y-0.4, table_text, fontsize=8, fontfamily='monospace',
         ha='center', va='center', color=dark_gray)

# Recommendations example
rec_example_box = FancyBboxPatch((8.5, output_y-1), 6, 1.5, 
                                 boxstyle="round,pad=0.05", 
                                 facecolor=light_gray, 
                                 edgecolor=dark_gray, 
                                 alpha=0.9)
ax2.add_patch(rec_example_box)
ax2.text(11.5, output_y+0.2, 'Optimization Recommendations', fontsize=11, fontweight='bold', 
         ha='center', va='center', color=dark_gray)
rec_text = '''• Downsize i-1234567 (t3.large → t3.medium)
• Enable S3 lifecycle on bucket-xyz
• Terminate idle EBS volume vol-abc123
• Consider Savings Plan for 20% savings'''
ax2.text(11.5, output_y-0.4, rec_text, fontsize=8,
         ha='center', va='center', color=dark_gray)

# Add workflow arrows
workflow_arrows = [
    ((3.5, 10.2), (4.5, 10.2)),   # Step 1 to 2
    ((7, 10.2), (8, 10.2)),       # Step 2 to 3
    ((10.5, 10.2), (11.5, 10.2)), # Step 3 to 4
]

for start, end in workflow_arrows:
    arrow = patches.FancyArrowPatch(start, end,
                                   arrowstyle='->', mutation_scale=20, 
                                   color=dark_gray, alpha=0.7, linewidth=2)
    ax2.add_patch(arrow)

# Commands at bottom
commands_y = 2
ax2.text(8, commands_y+0.5, 'Available Commands', fontsize=16, fontweight='bold', ha='center', color=dark_gray)

command_examples = [
    'cloudwhisper analyze-costs --days 30 --service ec2',
    'cloudwhisper optimize --service ec2 --region us-east-1',
    'cloudwhisper find-idle --days 7',
    'cloudwhisper savings-plans'
]

y_pos = commands_y
for cmd in command_examples:
    ax2.text(8, y_pos, cmd, fontsize=10, fontfamily='monospace',
             ha='center', va='center', color=primary_blue,
             bbox=dict(boxstyle="round,pad=0.3", facecolor=light_gray, alpha=0.8))
    y_pos -= 0.4

plt.tight_layout()
plt.savefig('/mnt/c/Users/sidda/OneDrive/Desktop/Q-Developer-Challenge/cloudwhisper/cloudwhisper_workflow.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("CloudWhisper workflow diagram saved as 'cloudwhisper_workflow.png'")
