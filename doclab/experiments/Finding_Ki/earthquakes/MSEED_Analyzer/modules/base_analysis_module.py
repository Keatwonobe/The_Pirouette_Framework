
class BaseAnalysisModule:
    """Base class for analysis modules"""
    
    def __init__(self, analyzer):
        self.analyzer = analyzer
    
    def analyze(self, trace, processed_trace=None, **kwargs):
        """
        Analyze a trace for Ki-related phenomena
        
        Parameters:
        -----------
        trace : obspy.Trace
            The trace to analyze
        processed_trace : obspy.Trace or None
            A preprocessed version of the trace, if available
        
        Returns:
        --------
        list of AnalysisResult
            Analysis results, or empty list if no patterns found
        """
        raise NotImplementedError("Subclasses must implement analyze()")
    
    def get_name(self):
        """Get the name of the module"""
        return self.__class__.__name__
    
    def get_description(self):
        """Get a description of the module"""
        return self.__doc__ or "No description available"