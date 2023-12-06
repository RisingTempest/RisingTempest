import streamlit as st
import pandas as pd
import numpy as np

# Create a title for our app
st.title('Uber pickups in NYC')

# Data from url to download
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# Save a cache, so when we update the code only take time if there are new things
# If you import a new library you must need to run the code again in the command line 
@st.cache_data

# Function to only load the nrows that we specify
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# Make an exploratory view of the raw data as a dataframe
st.subheader('Raw data')
st.write(data)

# Create a bar char
st.subheader('Number of pickups by hour')
# Make a histogram using .dt.hour (datetime.hour), with a range that covers 24 hours
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# Plot the bar char
st.bar_chart(hist_values)

# Plot a map from all pickups
st.subheader('Map of all pickups')
st.map(data)

# Plot a map only for pickups at the hour in the slider
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# Tha same to show the raw data, but with a button to show/hide data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)