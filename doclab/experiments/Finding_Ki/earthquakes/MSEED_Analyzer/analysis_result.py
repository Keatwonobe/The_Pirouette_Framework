import json

class AnalysisResult:
    """Container for analysis results"""
    
    def __init__(self, trace_id=None, start_time=None, end_time=None):
        self.trace_id = trace_id
        self.start_time = start_time
        self.end_time = end_time
        self.metrics = {}
        self.patterns = {}
        self.plots = {}
        self.metadata = {}
    
    def add_metric(self, name, value):
        """Add a numeric metric to the result"""
        self.metrics[name] = value
        return self
    
    def add_pattern(self, name, data):
        """Add a detected pattern to the result"""
        self.patterns[name] = data
        return self
    
    def add_plot_data(self, name, data):
        """Add plot data to the result"""
        self.plots[name] = data
        return self
    
    def add_metadata(self, name, value):
        """Add metadata to the result"""
        self.metadata[name] = value
        return self
    
    def to_dict(self):
        """Convert to dictionary for storage/reporting"""
        result = {
            'trace_id': self.trace_id,
            'start_time': str(self.start_time) if self.start_time else None,
            'end_time': str(self.end_time) if self.end_time else None,
            'metrics': self.metrics,
            'metadata': self.metadata,
        }
        
        # Only include patterns that are serializable
        serializable_patterns = {}
        for name, pattern in self.patterns.items():
            try:
                # Test if it can be serialized
                json.dumps(pattern)
                serializable_patterns[name] = pattern
            except (TypeError, OverflowError):
                # If not serializable, store a description instead
                if hasattr(pattern, '__len__'):
                    serializable_patterns[name] = f"<{type(pattern).__name__} with {len(pattern)} items>"
                else:
                    serializable_patterns[name] = f"<{type(pattern).__name__}>"
        
        result['patterns'] = serializable_patterns
        return result

