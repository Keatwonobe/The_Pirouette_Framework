from obspy.clients.fdsn import Client
from obspy import UTCDateTime

# Initialize the IRIS FDSN client
client = Client("IRIS")

# Define the time window for the Tohoku earthquake (adjust as needed for full coda)
# Main shock: 2011-03-11T05:46:23 UTC
t0 = UTCDateTime("2011-03-11T05:00:00")
t1 = UTCDateTime("2011-03-11T07:00:00")

# Station details: IU network, ANMO station, 00 location, BHZ channel (Broadband High Gain, Z-component)
network = "IU"
station = "ANMO"
location = "00"
channel = "BHZ"

print(f"Attempting to fetch waveforms for {network}.{station}.{location}.{channel} from {t0} to {t1}...")

try:
    # Fetch the waveform data
    st = client.get_waveforms(network, station, location, channel, t0, t1)
    
    # Define the output filename
    output_filename = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Ki/Gyroscope Data/MSEED_Analyzer/tohoku_ANMO_BHZ_20110311_0500_0700.mseed"
    
    # Write the data to a MiniSEED file
    st.write(output_filename, format="MSEED")
    print(f"Successfully downloaded and saved data to {output_filename}")

except Exception as e:
    print(f"Error fetching or saving waveform data: {e}")
    print("Please ensure 'obspy' is installed (pip install obspy) and you have an active internet connection.")