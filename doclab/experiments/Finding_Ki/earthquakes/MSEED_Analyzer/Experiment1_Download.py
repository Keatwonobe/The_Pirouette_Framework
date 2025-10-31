import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta

# Import ObsPy modules for seismic data handling
try:
    from obspy import UTCDateTime
    from obspy.clients.fdsn import Client, RoutingClient
    from obspy.clients.fdsn.header import FDSNException
except ImportError:
    print("Error: ObsPy is required for this application.")
    print("Please install it using: pip install obspy")
    sys.exit(1)

class ObsPyDownloaderApp:
    """Advanced GUI application for downloading seismic data using ObsPy"""
    
    # Available FDSN data centers
    DATA_CENTERS = [
        "IRIS", "USGS", "GEOFON", "INGV", "NCEDC", "RESIF", 
        "SCEDC", "GFZ", "ICGC", "NIEP", "ODC", "ETH", 
        "GEONET", "IRISPH5", "LMU", "ORFEUS", "RESIF", 
        "EMSC", "BGR", "USP"
    ]
    
    # Common file formats for seismic data
    OUTPUT_FORMATS = [
        "MSEED", "SAC", "SEGY", "WAV"
    ]
    
    def __init__(self, root):
        """Initialize the application with the root window"""
        self.root = root
        self.root.title("ObsPy Waveform Downloader")
        self.root.geometry("700x750")
        self.root.resizable(True, True)
    
        # Set application icon if available
        try:
            self.root.iconbitmap("seismic_icon.ico")
        except:
            pass
        
        # Variables to store user input
        self.data_center_var = tk.StringVar(value="IRIS")
        self.network_var = tk.StringVar(value="IU")
        self.station_var = tk.StringVar(value="ANMO")
        self.location_var = tk.StringVar(value="00")
        self.channel_var = tk.StringVar(value="BHZ")
        self.format_var = tk.StringVar(value="MSEED")
        self.output_path_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "output.mseed"))
        self.routing_var = tk.BooleanVar(value=False)
    
        # Time variables with default values
        self.start_year_var = tk.IntVar(value=datetime.now().year)
        self.start_month_var = tk.IntVar(value=datetime.now().month)
        self.start_day_var = tk.IntVar(value=datetime.now().day)
        self.start_hour_var = tk.IntVar(value=0)
        self.start_minute_var = tk.IntVar(value=0)
        self.start_second_var = tk.IntVar(value=0)
    
        # End time defaults to one hour from start
        self.end_year_var = tk.IntVar(value=datetime.now().year)
        self.end_month_var = tk.IntVar(value=datetime.now().month)
        self.end_day_var = tk.IntVar(value=datetime.now().day)
        self.end_hour_var = tk.IntVar(value=1)
        self.end_minute_var = tk.IntVar(value=0)
        self.end_second_var = tk.IntVar(value=0)
    
        # Status and progress variables
        self.download_in_progress = False
        self.status_var = tk.StringVar(value="Ready")  # Move this line BEFORE create_widgets
    
        # Create the UI elements
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all UI widgets"""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create tabs
        basic_tab = ttk.Frame(notebook)
        advanced_tab = ttk.Frame(notebook)
        help_tab = ttk.Frame(notebook)
        
        notebook.add(basic_tab, text="Basic Settings")
        notebook.add(advanced_tab, text="Advanced Options")
        notebook.add(help_tab, text="Help")
        
        # ===== Basic Settings Tab =====
        self.setup_basic_tab(basic_tab)
        
        # ===== Advanced Settings Tab =====
        self.setup_advanced_tab(advanced_tab)
        
        # ===== Help Tab =====
        self.setup_help_tab(help_tab)
        
        # Status bar at the bottom
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        status_label = ttk.Label(status_frame, text="Status:")
        status_label.pack(side=tk.LEFT)
        
        status_value = ttk.Label(status_frame, textvariable=self.status_var)
        status_value.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Action buttons at the bottom
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        download_button = ttk.Button(button_frame, text="Download Data", command=self.start_download)
        download_button.pack(side=tk.RIGHT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Settings", command=self.clear_settings)
        clear_button.pack(side=tk.RIGHT, padx=5)
        
    def setup_basic_tab(self, parent):
        """Setup widgets for the basic settings tab"""
        # Use grid layout manager for better control
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=3)
        
        # Data center selection
        ttk.Label(parent, text="Data Center:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        datacenter_combo = ttk.Combobox(parent, textvariable=self.data_center_var, values=self.DATA_CENTERS)
        datacenter_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Use Routing Client checkbox (fetches data from multiple data centers)
        routing_check = ttk.Checkbutton(parent, text="Use Routing Client (federated search)", variable=self.routing_var)
        routing_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5, padx=5)
        
        # Station parameters frame
        station_frame = ttk.LabelFrame(parent, text="Station Parameters")
        station_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10, padx=5)
        
        # Network
        ttk.Label(station_frame, text="Network Code:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Entry(station_frame, textvariable=self.network_var).grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        ttk.Label(station_frame, text="(e.g., IU, US, TA)").grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
        
        # Station
        ttk.Label(station_frame, text="Station Code:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Entry(station_frame, textvariable=self.station_var).grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        ttk.Label(station_frame, text="(e.g., ANMO, COLA)").grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
        
        # Location
        ttk.Label(station_frame, text="Location Code:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Entry(station_frame, textvariable=self.location_var).grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)
        ttk.Label(station_frame, text="(e.g., 00, 01, or -- for blank)").grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)
        
        # Channel
        ttk.Label(station_frame, text="Channel Code:").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        ttk.Entry(station_frame, textvariable=self.channel_var).grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)
        ttk.Label(station_frame, text="(e.g., BHZ, HHN, LHE)").grid(row=3, column=2, sticky=tk.W, pady=5, padx=5)
        
        # Time range frame
        time_frame = ttk.LabelFrame(parent, text="Time Range")
        time_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10, padx=5)
        
        # Start time
        start_time_frame = ttk.Frame(time_frame)
        start_time_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(start_time_frame, text="Start Time:").pack(side=tk.LEFT, padx=5)
        
        # Year
        ttk.Label(start_time_frame, text="Year:").pack(side=tk.LEFT, padx=(10, 0))
        year_spinner = ttk.Spinbox(start_time_frame, from_=1970, to=2030, width=5, textvariable=self.start_year_var)
        year_spinner.pack(side=tk.LEFT)
        
        # Month
        ttk.Label(start_time_frame, text="Month:").pack(side=tk.LEFT, padx=(10, 0))
        month_spinner = ttk.Spinbox(start_time_frame, from_=1, to=12, width=3, textvariable=self.start_month_var)
        month_spinner.pack(side=tk.LEFT)
        
        # Day
        ttk.Label(start_time_frame, text="Day:").pack(side=tk.LEFT, padx=(10, 0))
        day_spinner = ttk.Spinbox(start_time_frame, from_=1, to=31, width=3, textvariable=self.start_day_var)
        day_spinner.pack(side=tk.LEFT)
        
        # Hour, minute, second
        ttk.Label(start_time_frame, text="Time:").pack(side=tk.LEFT, padx=(10, 0))
        hour_spinner = ttk.Spinbox(start_time_frame, from_=0, to=23, width=3, textvariable=self.start_hour_var)
        hour_spinner.pack(side=tk.LEFT)
        ttk.Label(start_time_frame, text=":").pack(side=tk.LEFT)
        minute_spinner = ttk.Spinbox(start_time_frame, from_=0, to=59, width=3, textvariable=self.start_minute_var)
        minute_spinner.pack(side=tk.LEFT)
        ttk.Label(start_time_frame, text=":").pack(side=tk.LEFT)
        second_spinner = ttk.Spinbox(start_time_frame, from_=0, to=59, width=3, textvariable=self.start_second_var)
        second_spinner.pack(side=tk.LEFT)
        
        # End time
        end_time_frame = ttk.Frame(time_frame)
        end_time_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(end_time_frame, text="End Time:  ").pack(side=tk.LEFT, padx=5)
        
        # Year
        ttk.Label(end_time_frame, text="Year:").pack(side=tk.LEFT, padx=(10, 0))
        year_spinner = ttk.Spinbox(end_time_frame, from_=1970, to=2030, width=5, textvariable=self.end_year_var)
        year_spinner.pack(side=tk.LEFT)
        
        # Month
        ttk.Label(end_time_frame, text="Month:").pack(side=tk.LEFT, padx=(10, 0))
        month_spinner = ttk.Spinbox(end_time_frame, from_=1, to=12, width=3, textvariable=self.end_month_var)
        month_spinner.pack(side=tk.LEFT)
        
        # Day
        ttk.Label(end_time_frame, text="Day:").pack(side=tk.LEFT, padx=(10, 0))
        day_spinner = ttk.Spinbox(end_time_frame, from_=1, to=31, width=3, textvariable=self.end_day_var)
        day_spinner.pack(side=tk.LEFT)
        
        # Hour, minute, second
        ttk.Label(end_time_frame, text="Time:").pack(side=tk.LEFT, padx=(10, 0))
        hour_spinner = ttk.Spinbox(end_time_frame, from_=0, to=23, width=3, textvariable=self.end_hour_var)
        hour_spinner.pack(side=tk.LEFT)
        ttk.Label(end_time_frame, text=":").pack(side=tk.LEFT)
        minute_spinner = ttk.Spinbox(end_time_frame, from_=0, to=59, width=3, textvariable=self.end_minute_var)
        minute_spinner.pack(side=tk.LEFT)
        ttk.Label(end_time_frame, text=":").pack(side=tk.LEFT)
        second_spinner = ttk.Spinbox(end_time_frame, from_=0, to=59, width=3, textvariable=self.end_second_var)
        second_spinner.pack(side=tk.LEFT)
        
        # Preset time buttons
        preset_frame = ttk.Frame(time_frame)
        preset_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(preset_frame, text="Last Hour", command=lambda: self.set_time_preset("hour")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Last Day", command=lambda: self.set_time_preset("day")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Last Week", command=lambda: self.set_time_preset("week")).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_frame, text="Last Month", command=lambda: self.set_time_preset("month")).pack(side=tk.LEFT, padx=5)
        
        # Output file settings
        output_frame = ttk.LabelFrame(parent, text="Output Settings")
        output_frame.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=10, padx=5)
        
        # Format selection
        ttk.Label(output_frame, text="Format:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        format_combo = ttk.Combobox(output_frame, textvariable=self.format_var, values=self.OUTPUT_FORMATS)
        format_combo.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        # Output path
        ttk.Label(output_frame, text="Output File:").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        
        path_frame = ttk.Frame(output_frame)
        path_frame.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)
        
        path_entry = ttk.Entry(path_frame, textvariable=self.output_path_var)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(path_frame, text="Browse...", command=self.browse_output_file)
        browse_button.pack(side=tk.RIGHT, padx=5)
        
    def setup_advanced_tab(self, parent):
        """Setup widgets for the advanced settings tab"""
        # Create a text widget for the explanation
        explanation = ttk.Label(parent, text="Advanced Options", font=("TkDefaultFont", 12, "bold"))
        explanation.pack(pady=10)
        
        # Additional options frame
        options_frame = ttk.Frame(parent)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Metadata query section
        metadata_frame = ttk.LabelFrame(options_frame, text="Station/Response Metadata")
        metadata_frame.pack(fill=tk.X, pady=5)
        
        self.metadata_var = tk.BooleanVar(value=False)
        metadata_check = ttk.Checkbutton(metadata_frame, 
                                         text="Download station metadata along with waveforms",
                                         variable=self.metadata_var)
        metadata_check.pack(anchor=tk.W, padx=5, pady=5)
        
        self.resp_var = tk.BooleanVar(value=False)
        resp_check = ttk.Checkbutton(metadata_frame, 
                                     text="Include instrument response information",
                                     variable=self.resp_var)
        resp_check.pack(anchor=tk.W, padx=5, pady=5)
        
        # Processing options
        process_frame = ttk.LabelFrame(options_frame, text="Data Processing")
        process_frame.pack(fill=tk.X, pady=5)
        
        self.detrend_var = tk.BooleanVar(value=False)
        detrend_check = ttk.Checkbutton(process_frame, 
                                       text="Apply detrend to data",
                                       variable=self.detrend_var)
        detrend_check.pack(anchor=tk.W, padx=5, pady=5)
        
        self.filter_var = tk.BooleanVar(value=False)
        filter_check = ttk.Checkbutton(process_frame, 
                                      text="Apply bandpass filter",
                                      variable=self.filter_var)
        filter_check.pack(anchor=tk.W, padx=5, pady=5)
        
        filter_frame = ttk.Frame(process_frame)
        filter_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(filter_frame, text="Frequency Range:").grid(row=0, column=0, padx=5)
        
        self.freqmin_var = tk.DoubleVar(value=0.01)
        self.freqmax_var = tk.DoubleVar(value=10.0)
        
        freqmin_spinner = ttk.Spinbox(filter_frame, from_=0.001, to=100, increment=0.01, 
                                     width=6, textvariable=self.freqmin_var)
        freqmin_spinner.grid(row=0, column=1, padx=5)
        
        ttk.Label(filter_frame, text="to").grid(row=0, column=2, padx=5)
        
        freqmax_spinner = ttk.Spinbox(filter_frame, from_=0.001, to=100, increment=0.01, 
                                     width=6, textvariable=self.freqmax_var)
        freqmax_spinner.grid(row=0, column=3, padx=5)
        
        ttk.Label(filter_frame, text="Hz").grid(row=0, column=4, padx=5)
        
        # Plot options
        plot_frame = ttk.LabelFrame(options_frame, text="Visualization")
        plot_frame.pack(fill=tk.X, pady=5)
        
        self.plot_var = tk.BooleanVar(value=True)
        plot_check = ttk.Checkbutton(plot_frame, 
                                    text="Plot waveforms after download",
                                    variable=self.plot_var)
        plot_check.pack(anchor=tk.W, padx=5, pady=5)
        
        # API connection options
        conn_frame = ttk.LabelFrame(options_frame, text="Connection Options")
        conn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(conn_frame, text="Timeout (seconds):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.timeout_var = tk.IntVar(value=120)
        timeout_spinner = ttk.Spinbox(conn_frame, from_=30, to=600, increment=10, 
                                     width=5, textvariable=self.timeout_var)
        timeout_spinner.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
    def setup_help_tab(self, parent):
        """Setup widgets for the help tab"""
        help_text = tk.Text(parent, wrap=tk.WORD, width=80, height=20)
        help_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(help_text, command=help_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        help_text.config(yscrollcommand=scrollbar.set)
        
        # Help content
        help_content = """
ObsPy Waveform Downloader Help

This application allows you to download seismic waveform data from various data centers using ObsPy.

Basic Settings:
- Data Center: The FDSN data center to query for data.
- Use Routing Client: Enable this to search across multiple data centers.
- Network Code: The seismic network code (e.g., IU, US, TA).
- Station Code: The station identifier (e.g., ANMO, COLA).
- Location Code: The location code (typically 00, 01, or -- for blank).
- Channel Code: The channel identifier (e.g., BHZ, HHZ, LHZ).
  First letter: Band code (B=broadband, H=high, L=low)
  Second letter: Instrument code (H=high-gain seismometer)
  Third letter: Orientation code (Z=vertical, N=north-south, E=east-west)

Time Range:
- Select the start and end times for your data request.
- Use the preset buttons for quick time range selection.

Output Settings:
- Format: Select the desired output format (MSEED, SAC, etc.).
- Output File: Specify where to save the downloaded data.

Advanced Options:
- Metadata: Download station metadata along with waveforms.
- Response: Include instrument response information.
- Processing: Apply detrending or filtering to the data.
- Visualization: Plot waveforms after download.
- Connection: Configure timeout and connection settings.

Tips:
- Requests that are too large may timeout or be rejected.
- Some data centers have restrictions on data access.
- For large time ranges, consider downloading data in smaller chunks.
- Use the bandpass filter to reduce noise in your data.

For more information about ObsPy, visit: https://docs.obspy.org/
        """
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  # Make read-only
        
    def browse_output_file(self):
        """Open a file dialog to select the output file location"""
        # Get the current file extension
        current_path = self.output_path_var.get()
        current_ext = os.path.splitext(current_path)[1]
        
        # Set the initial file extension based on format
        format_ext = ".mseed"
        format_val = self.format_var.get().lower()
        
        if format_val == "sac":
            format_ext = ".sac"
        elif format_val == "segy":
            format_ext = ".segy"
        elif format_val == "wav":
            format_ext = ".wav"
            
        # Update filename if the format changed
        if current_ext != format_ext:
            current_path = os.path.splitext(current_path)[0] + format_ext
            
        # Open file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=format_ext,
            filetypes=[
                ("MiniSEED files", "*.mseed"),
                ("SAC files", "*.sac"),
                ("SEGY files", "*.segy"),
                ("WAV files", "*.wav"),
                ("All files", "*.*")
            ],
            initialfile=os.path.basename(current_path),
            initialdir=os.path.dirname(current_path)
        )
        
        # Update the path if a file was selected
        if file_path:
            self.output_path_var.set(file_path)
            
    def set_time_preset(self, preset):
        """Set time presets for common time ranges"""
        now = datetime.now()
        
        # Set end time to now
        self.end_year_var.set(now.year)
        self.end_month_var.set(now.month)
        self.end_day_var.set(now.day)
        self.end_hour_var.set(now.hour)
        self.end_minute_var.set(now.minute)
        self.end_second_var.set(now.second)
        
        # Calculate start time based on preset
        if preset == "hour":
            start_time = now - timedelta(hours=1)
        elif preset == "day":
            start_time = now - timedelta(days=1)
        elif preset == "week":
            start_time = now - timedelta(weeks=1)
        elif preset == "month":
            start_time = now - timedelta(days=30)
        else:
            return
            
        # Set start time
        self.start_year_var.set(start_time.year)
        self.start_month_var.set(start_time.month)
        self.start_day_var.set(start_time.day)
        self.start_hour_var.set(start_time.hour)
        self.start_minute_var.set(start_time.minute)
        self.start_second_var.set(start_time.second)
        
    def clear_settings(self):
        """Reset all settings to default values"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all settings?"):
            # Reset basic settings
            self.data_center_var.set("IRIS")
            self.network_var.set("IU")
            self.station_var.set("ANMO")
            self.location_var.set("00")
            self.channel_var.set("BHZ")
            self.format_var.set("MSEED")
            self.routing_var.set(False)
            
            # Reset time to current time and one hour before
            now = datetime.now()
            hour_ago = now - timedelta(hours=1)
            
            # Start time (hour ago)
            self.start_year_var.set(hour_ago.year)
            self.start_month_var.set(hour_ago.month)
            self.start_day_var.set(hour_ago.day)
            self.start_hour_var.set(hour_ago.hour)
            self.start_minute_var.set(hour_ago.minute)
            self.start_second_var.set(hour_ago.second)
            
            # End time (now)
            self.end_year_var.set(now.year)
            self.end_month_var.set(now.month)
            self.end_day_var.set(now.day)
            self.end_hour_var.set(now.hour)
            self.end_minute_var.set(now.minute)
            self.end_second_var.set(now.second)
            
            # Reset advanced options
            self.metadata_var.set(False)
            self.resp_var.set(False)
            self.detrend_var.set(False)
            self.filter_var.set(False)
            self.freqmin_var.set(0.01)
            self.freqmax_var.set(10.0)
            self.plot_var.set(True)
            self.timeout_var.set(120)
            
            # Reset output path
            self.output_path_var.set(os.path.join(os.path.expanduser("~"), "output.mseed"))
            
            # Update status
            self.status_var.set("Settings reset to defaults")
            
    def update_progress(self, value, status_text=None):
        """Update the progress bar and status text"""
        self.progress_var.set(value)
        if status_text:
            self.status_var.set(status_text)
        self.root.update_idletasks()
        
    def get_utc_datetime(self, year, month, day, hour, minute, second):
        """Convert date and time variables to an ObsPy UTCDateTime object"""
        try:
            date_str = f"{year}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"
            return UTCDateTime(date_str)
        except Exception as e:
            raise ValueError(f"Invalid date/time: {e}")
            
    def start_download(self):
        """Start the download process in a separate thread"""
        # Check if download already in progress
        if self.download_in_progress:
            messagebox.showinfo("Info", "Download already in progress")
            return
            
        # Validate inputs
        try:
            # Create UTCDateTime objects for start and end times
            starttime = self.get_utc_datetime(
                self.start_year_var.get(),
                self.start_month_var.get(),
                self.start_day_var.get(),
                self.start_hour_var.get(),
                self.start_minute_var.get(),
                self.start_second_var.get()
            )
            
            endtime = self.get_utc_datetime(
                self.end_year_var.get(),
                self.end_month_var.get(),
                self.end_day_var.get(),
                self.end_hour_var.get(),
                self.end_minute_var.get(),
                self.end_second_var.get()
            )
            
            # Validate time range
            if endtime <= starttime:
                raise ValueError("End time must be after start time")
                
            # Validate output path
            output_path = self.output_path_var.get()
            output_dir = os.path.dirname(output_path)
            
            if output_dir and not os.path.exists(output_dir):
                if messagebox.askyesno("Directory Not Found", 
                                      f"The directory '{output_dir}' does not exist. Create it?"):
                    os.makedirs(output_dir)
                else:
                    return
                    
        except Exception as e:
            messagebox.showerror("Validation Error", str(e))
            return
            
        # Start download in a separate thread
        self.download_in_progress = True
        self.update_progress(0, "Starting download...")
        
        download_thread = threading.Thread(target=self.perform_download, 
                                          args=(starttime, endtime, output_path))
        download_thread.daemon = True
        download_thread.start()
        
    def perform_download(self, starttime, endtime, output_path):
        """Perform the actual download (runs in a separate thread)"""
        try:
            self.update_progress(10, "Connecting to data center...")
            
            # Get client (regular or routing)
            if self.routing_var.get():
                client = RoutingClient("iris-federator")
            else:
                client = Client(self.data_center_var.get(), timeout=self.timeout_var.get())
                
            # Get network, station, location, channel parameters
            network = self.network_var.get()
            station = self.station_var.get()
            location = self.location_var.get()
            if location.lower() == "--":  # Handle blank location code
                location = ""
            channel = self.channel_var.get()
            
            self.update_progress(30, "Requesting waveform data...")
            
            # Get waveforms
            st = client.get_waveforms(
                network=network,
                station=station,
                location=location,
                channel=channel,
                starttime=starttime,
                endtime=endtime
            )
            
            # Get metadata if requested
            if self.metadata_var.get():
                self.update_progress(50, "Requesting station metadata...")
                inventory = client.get_stations(
                    network=network,
                    station=station,
                    location=location,
                    channel=channel,
                    starttime=starttime,
                    endtime=endtime,
                    level="response" if self.resp_var.get() else "channel"
                )
                
                # Save metadata to StationXML file
                metadata_path = os.path.splitext(output_path)[0] + ".xml"
                inventory.write(metadata_path, format="STATIONXML")
                
            self.update_progress(70, "Processing data...")
            
            # Apply processing if requested
            if len(st) > 0:
                if self.detrend_var.get():
                    st.detrend("linear")
                    
                if self.filter_var.get():
                    try:
                        freqmin = self.freqmin_var.get()
                        freqmax = self.freqmax_var.get()
                        st.filter("bandpass", freqmin=freqmin, freqmax=freqmax)
                    except Exception as e:
                        messagebox.showwarning("Filter Warning", f"Error applying filter: {e}")
            
            self.update_progress(80, "Saving data...")
            
            # Save waveforms
            output_format = self.format_var.get().upper()
            if output_format == "WAV":
                output_format = "WAV"  # ObsPy uses uppercase for this format
                
            st.write(output_path, format=output_format)
            
            self.update_progress(90, "Finalizing...")
            
            # Display plot if requested
            if self.plot_var.get() and len(st) > 0:
                self.plot_waveforms(st)
                
            # Show success message
            self.update_progress(100, "Download complete")
            messagebox.showinfo("Success", f"Successfully downloaded data to {output_path}")
            
        except FDSNException as e:
            self.update_progress(0, "Error")
            error_message = str(e).split('\n')[0]  # Get the first line of the error
            messagebox.showerror("FDSN Web Service Error", error_message)
            
        except Exception as e:
            self.update_progress(0, "Error")
            messagebox.showerror("Download Error", str(e))
            
        finally:
            self.download_in_progress = False
            
    def plot_waveforms(self, stream):
        """Plot the downloaded waveforms using matplotlib"""
        try:
            # Import matplotlib in the function to avoid loading it unless needed
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # Create a new Toplevel window for the plot
            plot_window = tk.Toplevel(self.root)
            plot_window.title("Waveform Plot")
            plot_window.geometry("800x600")
            
            # Create figure and canvas
            fig = plt.figure(figsize=(10, 8))
            canvas = FigureCanvasTkAgg(fig, master=plot_window)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # Create toolbar
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            toolbar = NavigationToolbar2Tk(canvas, plot_window)
            toolbar.update()
            
            # Plot the stream
            stream.plot(fig=fig)
            canvas.draw()
            
            # Add buttons for saving and exporting
            button_frame = ttk.Frame(plot_window)
            button_frame.pack(fill=tk.X, padx=10, pady=5)
            
            save_button = ttk.Button(button_frame, text="Save Figure", 
                                   command=lambda: self.save_figure(fig))
            save_button.pack(side=tk.RIGHT, padx=5)
            
            # Add plot information
            info_frame = ttk.Frame(plot_window)
            info_frame.pack(fill=tk.X, padx=10, pady=5)
            
            # Get stream information
            trace_info = []
            for tr in stream:
                trace_info.append(f"{tr.id}: {tr.stats.npts} samples, {tr.stats.sampling_rate} Hz, "
                                 f"{tr.stats.starttime} to {tr.stats.endtime}")
                
            info_text = tk.Text(info_frame, wrap=tk.WORD, height=len(trace_info) + 1, width=80)
            info_text.pack(fill=tk.X, expand=True)
            info_text.insert(tk.END, "Traces in the stream:\n")
            
            for info in trace_info:
                info_text.insert(tk.END, info + "\n")
                
            info_text.config(state=tk.DISABLED)  # Make read-only
            
        except Exception as e:
            messagebox.showerror("Plot Error", f"Error creating plot: {e}")
            
    def save_figure(self, fig):
        """Save the figure to a file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                fig.savefig(file_path, dpi=300, bbox_inches="tight")
                messagebox.showinfo("Success", f"Figure saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving figure: {e}")

def main():
    root = tk.Tk()
    app = ObsPyDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()