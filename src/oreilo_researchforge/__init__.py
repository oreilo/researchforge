"""OREiLO ResearchForge: traceable web research."""
from .models import ResearchConfig, ResearchReport, ResearchSource
from .pipeline import ResearchEngine
__version__ = "2.0.0"
__all__ = ["ResearchConfig", "ResearchReport", "ResearchSource", "ResearchEngine"]
