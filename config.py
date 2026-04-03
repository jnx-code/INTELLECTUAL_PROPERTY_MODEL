"""
Configuration settings for the AI Copyright Detection System.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class SystemConfig:
    """System-wide configuration parameters."""
    
    # Embedding model configuration
    text_embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    
    # Similarity thresholds
    high_risk_threshold: float = 0.85
    medium_risk_threshold: float = 0.70
    low_risk_threshold: float = 0.55
    
    # Search configuration
    top_k_results: int = 5
    
    # Content categories
    content_types: List[str] = None
    
    def __post_init__(self):
        if self.content_types is None:
            self.content_types = ["book", "article", "song", "poem", "code", "script"]


@dataclass
class RiskLevel:
    """Risk level definitions."""
    HIGH: str = "HIGH"
    MEDIUM: str = "MEDIUM"
    LOW: str = "LOW"
    NONE: str = "NONE"


# Global configuration instance
CONFIG = SystemConfig()
RISK = RiskLevel()
