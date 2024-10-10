import streamlit as st
import pandas as pd

st.title("Analytics Dashboard")



df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv")

st.write(df.head())
# Create Interactive Analytics Dashboard
st.header("Interactive Analytics Dashboard")
st.write("This is an interactive analytics dashboard, where you can select a continent and see the data for that continent.")
st.write("You can also select a country and see the data for that country.")

# Create a selectbox for the continent
continent = st.selectbox("Select a Continent", df['continent'].unique())

# Filter the data for the selected continent
df_continent = df[df['continent'] == continent]

# Create a selectbox for the country
country = st.selectbox("Select a Country", df_continent['country'].unique())

# Filter the data for the selected country
df_country = df_continent[df_continent['country'] == country]

# Create a chart for the selected country
st.write("Life Expectancy at birth (years)")
st.line_chart(df_country.groupby('year')['lifeExp'].mean())

# Create a chart for the selected country
st.write("Population")
st.line_chart(df_country.groupby('year')['pop'].mean())

# Create a chart for the selected country
st.write("GDP per capita")
st.line_chart(df_country.groupby('year')['gdpPercap'].mean())
