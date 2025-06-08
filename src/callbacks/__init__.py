from .pipeline_callbacks import register_pipeline_callbacks
from .visualization_callbacks import register_visualization_callbacks
from .metrics_callbacks import register_metrics_callbacks

def register_callbacks(app):
    """Register all callbacks for the application."""
    register_pipeline_callbacks(app)
    register_visualization_callbacks(app)
    register_metrics_callbacks(app) 