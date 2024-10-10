import streamlit as st
import pandas as pd

st.title("Second Page")

st.write("This is the second page of the app")

st.header("Interactive Analytics Dashboard")

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv")

df.rename(columns={'long': 'lon'}, inplace=True)

st.write(df.sample(5))

st.map(df)
