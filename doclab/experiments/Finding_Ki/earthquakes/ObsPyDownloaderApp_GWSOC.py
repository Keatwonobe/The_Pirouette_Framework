import os
import numpy as np
from pathlib import Path
from gwpy.timeseries import TimeSeries
from obspy import Stream, Trace, UTCDateTime
import argparse
from gwosc.locate import get_urls
from gwosc import datasets

def fetch_gw_data(event_name=None, detector=None, start_time=None, end_time=None, 
                 duration=None, sample_rate=4096, output_dir='gw_data'):
    """
    Fetch gravitational wave data from GWOSC and save as MSEED format.
    
    Parameters:
    -----------
    event_name : str, optional
        Name of the gravitational wave event (e.g., 'GW150914')
    detector : str, optional
        Detector name ('H1', 'L1', or 'V1')
    start_time : str or float, optional
        GPS start time or ISO format time (required if event_name not provided)
    end_time : str or float, optional
        GPS end time or ISO format time (can be replaced by duration)
    duration : float, optional
        Duration in seconds (required if end_time not provided)
    sample_rate : int, optional
        Sample rate in Hz (default: 4096)
    output_dir : str, optional
        Directory to save MSEED files (default: 'gw_data')
    
    Returns:
    --------
    list
        Paths to generated MSEED files
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    mseed_files = []
    
    # Determine detectors list
    if detector:
        detectors = [detector]
    else:
        detectors = ['H1', 'L1', 'V1']  # LIGO Hanford, LIGO Livingston, Virgo
    
    # Handle time calculations first
    if event_name:
        # Get event information
        try:
            # Get event data using gwosc
            events = datasets.find_datasets(type='events')
            if event_name not in events:
                print(f"Event {event_name} not found in GWOSC events catalog.")
                print(f"Available events: {', '.join(events)}")
                return []
            
            # Get event data and time range
            event_data = datasets.event_gps(event_name)
            _start_time = event_data - 15  # 15 seconds before event
            _duration = 30  # 30 seconds total
            _end_time = _start_time + _duration
            
        except Exception as e:
            print(f"Error getting event data for {event_name}: {e}")
            return []
    else:
        # Use provided time range
        if start_time is None:
            print("Must provide either event_name or start_time")
            return []
        
        # Convert start_time to float if it's a string
        if isinstance(start_time, str):
            try:
                if 'T' in start_time:  # ISO format
                    from astropy.time import Time
                    _start_time = Time(start_time).gps
                else:  # GPS time as string
                    _start_time = float(start_time)
            except Exception as e:
                print(f"Error parsing start_time: {e}")
                return []
        else:
            _start_time = float(start_time)
        
        # Handle end_time or duration
        if end_time is not None:
            if isinstance(end_time, str):
                try:
                    if 'T' in end_time:  # ISO format
                        from astropy.time import Time
                        _end_time = Time(end_time).gps
                    else:  # GPS time as string
                        _end_time = float(end_time)
                except Exception as e:
                    print(f"Error parsing end_time: {e}")
                    return []
            else:
                _end_time = float(end_time)
            
            _duration = _end_time - _start_time
        elif duration is not None:
            _duration = float(duration)
            _end_time = _start_time + _duration
        else:
            print("Must provide either end_time or duration")
            return []
    
    # Now fetch data for each detector
    for det in detectors:
        try:
            print(f"Fetching {det} data from {_start_time} to {_end_time}...")
            
            # Use the TimeSeries.fetch_open_data method
            ts = TimeSeries.fetch_open_data(det, _start_time, _end_time)
            
            if ts is None or len(ts) == 0:
                print(f"No data available for {det} in the specified time range")
                continue
            
            # Resample if needed
            if ts.sample_rate.value != sample_rate:
                print(f"Resampling from {ts.sample_rate.value} Hz to {sample_rate} Hz...")
                ts = ts.resample(sample_rate)
            
            # Convert to ObsPy trace
            trace = Trace(data=ts.value)
            
            # Set trace metadata
            trace.stats.network = "GW"
            trace.stats.station = det
            trace.stats.channel = "STRAIN"  # Standard for strain data
            
            # Set timing information - convert from GPS time to UTC
            start_utc = UTCDateTime(ts.t0.value)
            trace.stats.starttime = start_utc
            trace.stats.sampling_rate = sample_rate
            
            # Create stream and write MSEED
            stream = Stream(traces=[trace])
            
            # Generate filename
            if event_name:
                filename = f"{det}_{event_name}_STRAIN.mseed"
            else:
                filename = f"{det}_{int(_start_time)}_STRAIN.mseed"
            
            mseed_path = output_dir / filename
            stream.write(str(mseed_path), format="MSEED")
            
            print(f"Saved {mseed_path}")
            mseed_files.append(mseed_path)
            
        except Exception as e:
            print(f"Error fetching data for {det}: {e}")
            import traceback
            traceback.print_exc()
    
    return mseed_files

def run_ki_analysis(mseed_files, analysis_script="ki_mseed_analyzer_advanced_4.py",
                   ki_value=4.14159, significance=2.0, no_plots=False, 
                   output_dir=None):
    """
    Run the Ki resonance analysis on the generated MSEED files
    
    Parameters:
    -----------
    mseed_files : list
        List of MSEED file paths to analyze
    analysis_script : str
        Path to the Ki analysis script
    ki_value : float
        Ki value to use for analysis
    significance : float
        Significance threshold
    no_plots : bool
        Whether to disable plot generation
    output_dir : str or None
        Output directory for analysis results
    
    Returns:
    --------
    int
        Return code from the analysis process
    """
    import subprocess
    import sys
    
    # Build command
    cmd = [sys.executable, analysis_script]
    
    if len(mseed_files) == 1:
        # If single file
        cmd.append(str(mseed_files[0]))
    else:
        # If multiple files, use the directory
        cmd.append(str(Path(mseed_files[0]).parent))
    
    # Add options
    cmd.extend(['--ki-value', str(ki_value)])
    cmd.extend(['--significance', str(significance)])
    
    if no_plots:
        cmd.append('--no-plots')
    
    if output_dir:
        cmd.extend(['--output-dir', output_dir])
    
    # Run the command
    print(f"Running analysis command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    
    return result.returncode

def list_available_events():
    """List all available gravitational wave events in GWOSC"""
    try:
        events = datasets.find_datasets(type='events')
        print("\nAvailable gravitational wave events:")
        for i, event in enumerate(sorted(events), 1):
            # Get event GPS time for reference
            gps_time = datasets.event_gps(event)
            print(f"{i}. {event} (GPS: {gps_time})")
        print("\nUse --event [EVENT_NAME] to fetch data for a specific event")
    except Exception as e:
        print(f"Error listing events: {e}")

def main():
    parser = argparse.ArgumentParser(description='Fetch GW data and analyze with Ki resonance analyzer')
    
    # Data source options
    source_group = parser.add_mutually_exclusive_group(required=False)
    source_group.add_argument('--event', help='Gravitational wave event name (e.g., GW150914)')
    source_group.add_argument('--start-time', help='Start time (GPS or ISO format)')
    
    # Time range options (when not using event)
    parser.add_argument('--end-time', help='End time (GPS or ISO format)')
    parser.add_argument('--duration', type=float, help='Duration in seconds')
    
    # Data options
    parser.add_argument('--detector', choices=['H1', 'L1', 'V1'], 
                       help='Specific detector to use (default: fetch all)')
    parser.add_argument('--sample-rate', type=int, default=4096,
                       help='Sample rate in Hz (default: 4096)')
    
    # Output options
    parser.add_argument('--output-dir', default='gw_data',
                       help='Directory to save MSEED files (default: gw_data)')
    
    # Analysis options
    parser.add_argument('--analyze', action='store_true',
                       help='Run Ki resonance analysis on fetched data')
    parser.add_argument('--analysis-script', default='ki_mseed_analyzer_advanced_4.py',
                       help='Path to Ki analysis script (default: ki_mseed_analyzer_advanced_4.py)')
    parser.add_argument('--ki-value', type=float, default=4.14159,
                       help='Ki value for analysis (default: 4.14159)')
    parser.add_argument('--significance', type=float, default=2.0,
                       help='Significance threshold (default: 2.0)')
    parser.add_argument('--no-plots', action='store_true',
                       help='Disable plot generation in analysis')
    parser.add_argument('--analysis-output-dir', 
                       help='Output directory for analysis results')
    
    # Utility options
    parser.add_argument('--list-events', action='store_true',
                       help='List available gravitational wave events')
    
    args = parser.parse_args()
    
    # List events if requested
    if args.list_events:
        list_available_events()
        return 0
    
    # Check required args
    if not args.event and not args.start_time:
        parser.print_help()
        print("\nError: Must specify either --event or --start-time")
        print("Tip: Use --list-events to see available events")
        return 1
    
    # Fetch data
    mseed_files = fetch_gw_data(
        event_name=args.event,
        detector=args.detector,
        start_time=args.start_time,
        end_time=args.end_time,
        duration=args.duration,
        sample_rate=args.sample_rate,
        output_dir=args.output_dir
    )
    
    if not mseed_files:
        print("No data was successfully fetched. Exiting.")
        return 1
    
    # Run analysis if requested
    if args.analyze:
        return run_ki_analysis(
            mseed_files,
            analysis_script=args.analysis_script,
            ki_value=args.ki_value,
            significance=args.significance,
            no_plots=args.no_plots,
            output_dir=args.analysis_output_dir
        )
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())