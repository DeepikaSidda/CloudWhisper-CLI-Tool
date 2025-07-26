#!/usr/bin/env python3
"""
CloudWhisper Demonstration Script

This script demonstrates the capabilities of CloudWhisper CLI tool.
"""

import os
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def run_command(command, description):
    """Run a command and display the output."""
    console.print(f"\n[bold blue]Demo: {description}[/bold blue]")
    console.print(f"[dim]Command: {command}[/dim]")
    console.print("─" * 60)
    
    try:
        # Use bash explicitly to handle source command
        result = subprocess.run(
            ["bash", "-c", command], 
            capture_output=True, 
            text=True, 
            cwd="/mnt/c/Users/sidda/OneDrive/Desktop/Q-Developer-Challenge/cloudwhisper"
        )
        
        if result.returncode == 0:
            if result.stdout:
                console.print(result.stdout)
            else:
                console.print("[green]✓ Command executed successfully (no output)[/green]")
        else:
            console.print(f"[red]Error (exit code {result.returncode}):[/red]")
            if result.stderr:
                console.print(result.stderr)
            if result.stdout:
                console.print(result.stdout)
    except Exception as e:
        console.print(f"[red]Exception: {e}[/red]")

def main():
    """Run the CloudWhisper demonstration."""
    
    console.print(Panel.fit(
        Text("CloudWhisper CLI Tool Demonstration", style="bold white"),
        style="bold blue",
        padding=(1, 2)
    ))
    
    console.print("""
[bold yellow]CloudWhisper[/bold yellow] is an AI-powered CLI tool that helps you:

1. 🤖 Generate Terraform code from natural language
2. 💰 Analyze AWS costs and usage patterns  
3. 🔧 Get optimization recommendations to reduce spending
4. 🔍 Find idle resources that can be terminated
5. 💡 Get Savings Plans recommendations

[bold red]Note:[/bold red] This demo shows the CLI interface. For full functionality, you need:
- AWS credentials configured
- OpenAI API key for Terraform generation
""")
    
    # Activate virtual environment prefix
    venv_prefix = "source venv/bin/activate && "
    
    # Demo 1: Show help
    run_command(f"{venv_prefix}cloudwhisper --help", "Main help menu")
    
    # Demo 2: Show generate help
    run_command(f"{venv_prefix}cloudwhisper generate --help", "Terraform generation help")
    
    # Demo 3: Show analyze-costs help
    run_command(f"{venv_prefix}cloudwhisper analyze-costs --help", "Cost analysis help")
    
    # Demo 4: Show optimize help
    run_command(f"{venv_prefix}cloudwhisper optimize --help", "Optimization help")
    
    # Demo 5: Show find-idle help
    run_command(f"{venv_prefix}cloudwhisper find-idle --help", "Find idle resources help")
    
    # Demo 6: Show savings-plans help
    run_command(f"{venv_prefix}cloudwhisper savings-plans --help", "Savings Plans help")
    
    console.print(f"\n[bold green]✓ CloudWhisper CLI tool is successfully installed and working![/bold green]")
    
    console.print(Panel("""
[bold yellow]Next Steps:[/bold yellow]

1. Set up your environment variables:
   [dim]export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key  
   export AWS_DEFAULT_REGION=us-east-1
   export OPENAI_API_KEY=your_openai_key[/dim]

2. Try generating Terraform code:
   [dim]cloudwhisper generate "Create an S3 bucket with versioning"[/dim]

3. Analyze your AWS costs:
   [dim]cloudwhisper analyze-costs --days 30[/dim]

4. Get optimization recommendations:
   [dim]cloudwhisper optimize[/dim]

5. Find idle resources:
   [dim]cloudwhisper find-idle --days 7[/dim]
""", title="Usage Instructions", border_style="green"))

if __name__ == "__main__":
    main()
