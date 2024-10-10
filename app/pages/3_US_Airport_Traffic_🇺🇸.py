import streamlit as st
import pandas as pd
import pydeck as pdk

# Section 2: United States Airport Traffic Analysis
st.title("United States Airport Traffic Analysis 🛩️")

# Load the US airport dataset
us_airport_df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv")
us_airport_df.rename(columns={'long': 'lon'}, inplace=True)

# Dictionary mapping state abbreviations to full names
state_names = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
    "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
}

# Add full state names to the DataFrame
us_airport_df['state_full'] = us_airport_df['state'].map(state_names)

# Display a sample of the data
st.write("Here’s a sample of the US airport traffic data:")
st.write(us_airport_df.sample(5))

# Display a map of US airport traffic using PyDeck
st.subheader("Airport Traffic Map")

# PyDeck configuration
view_state = pdk.ViewState(
    latitude=us_airport_df['lat'].mean(),
    longitude=us_airport_df['lon'].mean(),
    zoom=3,
    pitch=40,
)

layer = pdk.Layer(
    'ScatterplotLayer',
    data=us_airport_df,
    get_position='[lon, lat]',
    get_radius=10000,
    get_color='[200, 30, 0, 160]',
    pickable=True,
)

tooltip = {"html": "<b>Airport:</b> {airport}<br/><b>City:</b> {city}<br/><b>State:</b> {state_full}"}

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

st.pydeck_chart(r)

# Filter US airport data by state using full state names
st.subheader("Filter Airport Traffic by State")

selected_state = st.selectbox("Select a State", us_airport_df['state_full'].unique())
df_state = us_airport_df[us_airport_df['state_full'] == selected_state]

# Create a filtered map for the selected state
st.write(f"Airports in {selected_state}")
filtered_view_state = pdk.ViewState(
    latitude=df_state['lat'].mean(),
    longitude=df_state['lon'].mean(),
    zoom=6,
    pitch=40,
)

filtered_layer = pdk.Layer(
    'ScatterplotLayer',
    data=df_state,
    get_position='[lon, lat]',
    get_radius=10000,
    get_color='[0, 100, 200, 160]',
    pickable=True,
)

filtered_r = pdk.Deck(
    layers=[filtered_layer],
    initial_view_state=filtered_view_state,
    tooltip=tooltip
)

st.pydeck_chart(filtered_r)

# Highlight the busiest airport in the US dataset
st.subheader("Busiest Airport Information")

busiest_airport = us_airport_df.loc[us_airport_df['cnt'].idxmax()]

st.write(f"🛫 **Busiest Airport**: {busiest_airport['airport']} in {busiest_airport['city']}, {busiest_airport['state_full']}")
st.write(f"**Traffic Volume**: {busiest_airport['cnt']}")

# Traffic Volume by State
st.subheader("Traffic Volume by State")

# Summarize traffic data by state
df_state_traffic = us_airport_df.groupby('state_full')['cnt'].sum().reset_index()

# Display a bar chart
st.bar_chart(df_state_traffic.set_index('state_full'))

# Final Remarks
st.write("Explore both global and US-specific data interactively with this dashboard. Adjust the selections to view data trends and visualize traffic patterns dynamically.")
