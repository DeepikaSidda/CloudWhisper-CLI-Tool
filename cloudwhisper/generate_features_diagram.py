#!/usr/bin/env python3
"""
Generate CloudWhisper Features Overview Diagram
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle
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
aws_orange = '#FF9900'

# Title
ax.text(8, 11.5, 'CloudWhisper', 
        fontsize=28, fontweight='bold', ha='center', color=primary_blue)
ax.text(8, 11, 'Feature Overview & Benefits', 
        fontsize=16, ha='center', color=secondary_blue, style='italic')

# Central CloudWhisper logo/circle
center_circle = Circle((8, 7), 1.5, facecolor=primary_blue, edgecolor=dark_gray, 
                      linewidth=3, alpha=0.9)
ax.add_patch(center_circle)
ax.text(8, 7.2, 'CloudWhisper', fontsize=14, fontweight='bold', 
        ha='center', va='center', color='white')
ax.text(8, 6.8, 'CLI Tool', fontsize=12, 
        ha='center', va='center', color='white')

# Feature boxes around the center
features = [
    # (x, y, width, height, title, description, color)
    (2, 9.5, 3, 1.2, 'AI Code Generation', 'Natural language to\nTerraform code', green),
    (11, 9.5, 3, 1.2, 'Cost Analysis', 'AWS spending insights\nand trends', accent_orange),
    (2, 4.5, 3, 1.2, 'Resource Optimization', 'EC2, S3, RDS\nrightsizing', secondary_blue),
    (11, 4.5, 3, 1.2, 'Idle Detection', 'Find unused resources\nto save costs', red),
    (1, 7, 3, 1.2, 'Rich Output', 'Beautiful tables\nand visualizations', '#9C27B0'),
    (12, 7, 3, 1.2, 'Best Practices', 'Security & compliance\nbuilt-in', '#607D8B'),
]

for x, y, w, h, title, desc, color in features:
    # Feature box
    feature_box = FancyBboxPatch((x, y), w, h, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=color, 
                                 edgecolor=dark_gray, 
                                 linewidth=2,
                                 alpha=0.9)
    ax.add_patch(feature_box)
    
    # Feature title
    ax.text(x + w/2, y + h - 0.3, title, fontsize=12, fontweight='bold', 
            ha='center', va='center', color='white')
    
    # Feature description
    ax.text(x + w/2, y + 0.3, desc, fontsize=10, 
            ha='center', va='center', color='white')
    
    # Connection line to center
    center_x, center_y = 8, 7
    feature_center_x, feature_center_y = x + w/2, y + h/2
    
    # Calculate connection points
    dx = feature_center_x - center_x
    dy = feature_center_y - center_y
    distance = np.sqrt(dx**2 + dy**2)
    
    # Start point (edge of center circle)
    start_x = center_x + (dx / distance) * 1.5
    start_y = center_y + (dy / distance) * 1.5
    
    # End point (edge of feature box)
    if abs(dx) > abs(dy):  # Horizontal connection
        end_x = x if dx < 0 else x + w
        end_y = feature_center_y
    else:  # Vertical connection
        end_x = feature_center_x
        end_y = y if dy < 0 else y + h
    
    # Draw connection line
    line = patches.ConnectionPatch((start_x, start_y), (end_x, end_y), 
                                  "data", "data", arrowstyle='-', 
                                  color=color, alpha=0.6, linewidth=3)
    ax.add_artist(line)

# Benefits section
benefits_y = 2.5
ax.text(8, benefits_y + 0.8, 'Key Benefits', fontsize=18, fontweight='bold', ha='center', color=dark_gray)

benefits = [
    ('Faster Infrastructure Deployment', 'Generate production-ready Terraform in seconds'),
    ('Significant Cost Savings', 'Identify and eliminate wasteful spending'),
    ('Improved Productivity', 'Automate manual cost analysis tasks'),
    ('Better Decision Making', 'Data-driven optimization recommendations'),
]

benefit_colors = [primary_blue, accent_orange, green, secondary_blue]

x_positions = [1, 5, 9, 13]
for i, (benefit, desc) in enumerate(benefits):
    benefit_box = FancyBboxPatch((x_positions[i] - 1.5, benefits_y - 0.8), 3, 1.2, 
                                 boxstyle="round,pad=0.05", 
                                 facecolor=light_gray, 
                                 edgecolor=benefit_colors[i], 
                                 linewidth=2,
                                 alpha=0.9)
    ax.add_patch(benefit_box)
    
    ax.text(x_positions[i], benefits_y - 0.1, benefit, fontsize=10, fontweight='bold', 
            ha='center', va='center', color=benefit_colors[i])
    ax.text(x_positions[i], benefits_y - 0.5, desc, fontsize=8, 
            ha='center', va='center', color=dark_gray)

# Use cases at the bottom
use_cases_y = 0.8
ax.text(8, use_cases_y + 0.3, 'Perfect for DevOps Teams, Cloud Engineers, and Cost Optimization Specialists', 
        fontsize=12, ha='center', color=dark_gray, style='italic')

# Add some decorative elements
# AWS services icons (simplified)
aws_services = ['EC2', 'S3', 'RDS', 'Lambda', 'VPC']
service_colors = [aws_orange, green, primary_blue, accent_orange, secondary_blue]

for i, (service, color) in enumerate(zip(aws_services, service_colors)):
    angle = i * (2 * np.pi / len(aws_services))
    x = 8 + 3.5 * np.cos(angle)
    y = 7 + 3.5 * np.sin(angle)
    
    service_circle = Circle((x, y), 0.3, facecolor=color, edgecolor=dark_gray, 
                           alpha=0.7)
    ax.add_patch(service_circle)
    ax.text(x, y, service, fontsize=8, fontweight='bold', 
            ha='center', va='center', color='white')

plt.tight_layout()
plt.savefig('/mnt/c/Users/sidda/OneDrive/Desktop/Q-Developer-Challenge/cloudwhisper/cloudwhisper_features.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("CloudWhisper features diagram saved as 'cloudwhisper_features.png'")
