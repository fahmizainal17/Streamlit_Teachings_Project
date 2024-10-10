import streamlit as st
import pandas as pd

# Title
st.title("Analytics Dashboard 📊")

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv")

# Display the dataset
st.write("Here's a preview of the dataset:")
st.write(df.head())

# Interactive Analytics Dashboard Header
st.header("Interactive Analytics Dashboard")
st.write("This dashboard allows you to explore data interactively by selecting a continent and country. It displays key metrics such as life expectancy, population, and GDP per capita over time.")

# Continent selection
continent = st.selectbox("Select a Continent", df['continent'].unique())

# Filter data based on selected continent
df_continent = df[df['continent'] == continent]

# Country selection within the selected continent
country = st.selectbox("Select a Country", df_continent['country'].unique())

# Filter data based on selected country
df_country = df_continent[df_continent['country'] == country]

# Line charts for various metrics
st.subheader(f"Data for {country} in {continent}")

st.write("### Life Expectancy at Birth (Years)")
st.line_chart(df_country.groupby('year')['lifeExp'].mean())

st.write("### Population")
st.line_chart(df_country.groupby('year')['pop'].mean())

st.write("### GDP per Capita")
st.line_chart(df_country.groupby('year')['gdpPercap'].mean())

# Additional Interaction: Year Filter
st.header("Advanced Filtering Options")

# Year filter
year_range = st.slider("Select Year Range", min_value=int(df_country['year'].min()), max_value=int(df_country['year'].max()), value=(int(df_country['year'].min()), int(df_country['year'].max())))
df_country_filtered = df_country[(df_country['year'] >= year_range[0]) & (df_country['year'] <= year_range[1])]

st.write(f"Data for {country} from {year_range[0]} to {year_range[1]}")

# Filtered Line Charts
st.write("### Life Expectancy (Filtered)")
st.line_chart(df_country_filtered.groupby('year')['lifeExp'].mean())

st.write("### Population (Filtered)")
st.line_chart(df_country_filtered.groupby('year')['pop'].mean())

st.write("### GDP per Capita (Filtered)")
st.line_chart(df_country_filtered.groupby('year')['gdpPercap'].mean())

# Additional Chart: Comparison Between Countries
st.header("Comparison Between Countries")

# Multi-select box for countries
countries_selected = st.multiselect("Select countries to compare", df_continent['country'].unique(), default=[country])

# Filter data for the selected countries
df_countries = df_continent[df_continent['country'].isin(countries_selected)]

# Chart comparing life expectancy across selected countries
st.write("### Life Expectancy Comparison")
st.line_chart(df_countries.groupby(['year', 'country'])['lifeExp'].mean().unstack())

# Chart comparing GDP per capita across selected countries
st.write("### GDP per Capita Comparison")
st.line_chart(df_countries.groupby(['year', 'country'])['gdpPercap'].mean().unstack())

# Download Filtered Data
st.header("Download Filtered Data")

# Provide an option for users to download the filtered data
st.write("You can download the filtered data for further analysis.")
csv = df_country_filtered.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name=f'{country}_data_filtered.csv',
    mime='text/csv',
)

# Final Remarks
st.write("That's the end of this dashboard. 🎉 Explore more by changing the selections and viewing the dynamic changes!")
