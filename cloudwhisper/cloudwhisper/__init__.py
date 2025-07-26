"""
CloudWhisper - AI-powered AWS infrastructure and cost optimization CLI tool
"""

__version__ = "1.0.0"
__author__ = "CloudWhisper Team"
__email__ = "<email>"

from .infrawhisper import TerraformGenerator
from .cloudfuel import CostAnalyzer, CostOptimizer

__all__ = ["TerraformGenerator", "CostAnalyzer", "CostOptimizer"]
