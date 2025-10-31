from obspy import UTCDateTime
from obspy.clients.fdsn import Client

client = Client("IRIS")
starttime = UTCDateTime("2025-04-01T00:00:00")
endtime = UTCDateTime("2025-04-01T01:00:00")

# Replace 'IU', 'ANMO', '00', 'BHZ' with your desired network, station, location, and channel codes
st = client.get_waveforms(network="IU", station="ANMO", location="00", channel="BHZ",
                          starttime=starttime, endtime=endtime)

# Save the data to a MiniSEED file
st.write("output.mseed", format="MSEED")

