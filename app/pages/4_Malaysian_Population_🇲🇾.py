import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the Streamlit app title
st.title("Malaysian Population Data Dashboard 🇲🇾")

# Load the dataset
URL_DATA = 'https://storage.dosm.gov.my/population/population_malaysia.parquet'
df_malaysia = pd.read_parquet(URL_DATA)

# Convert 'date' column to datetime format
if 'date' in df_malaysia.columns:
    df_malaysia['date'] = pd.to_datetime(df_malaysia['date'])

# Sidebar filters for interaction
st.sidebar.header("Filter the Data:")
sex_filter = st.sidebar.multiselect("Select Gender:", options=df_malaysia['sex'].unique(), default=df_malaysia['sex'].unique())
age_filter = st.sidebar.multiselect("Select Age Group:", options=df_malaysia['age'].unique(), default=df_malaysia['age'].unique())
ethnicity_filter = st.sidebar.multiselect("Select Ethnicity:", options=df_malaysia['ethnicity'].unique(), default=df_malaysia['ethnicity'].unique())
year_filter = st.sidebar.slider("Select Year Range:", int(df_malaysia['date'].dt.year.min()), int(df_malaysia['date'].dt.year.max()), (int(df_malaysia['date'].dt.year.min()), int(df_malaysia['date'].dt.year.max())))

# Filter the data based on selections
filtered_data = df_malaysia[
    (df_malaysia['sex'].isin(sex_filter)) &
    (df_malaysia['age'].isin(age_filter)) &
    (df_malaysia['ethnicity'].isin(ethnicity_filter)) &
    (df_malaysia['date'].dt.year.between(year_filter[0], year_filter[1]))
]

# Create columns for layout
col1, col2 = st.columns(2)

# Display the filtered dataset in one column
with col1:
    st.write("### Filtered Dataset Preview:")
    st.write(filtered_data)

# Display summary statistics in the other column
with col2:
    st.write("### Summary Statistics")
    st.write(filtered_data.describe())

# Arrange visualizations in columns and rows
st.write("### Visualizations")

# Columns for population by age group and by ethnicity
col3, col4 = st.columns(2)

# Population distribution by age group
with col3:
    if 'age' in filtered_data.columns and 'population' in filtered_data.columns:
        st.subheader("Population Distribution by Age Group")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='age', y='population', data=filtered_data, hue='sex', ax=ax)
        plt.xticks(rotation=45)
        plt.title("Population Distribution by Age Group")
        plt.xlabel("Age Group")
        plt.ylabel("Population")
        st.pyplot(fig)

# Population distribution by ethnicity
with col4:
    if 'ethnicity' in filtered_data.columns and 'population' in filtered_data.columns:
        st.subheader("Population Distribution by Ethnicity")
        fig, ax = plt.subplots(figsize=(8, 5))
        ethnicity_dist = filtered_data.groupby('ethnicity')['population'].sum().reset_index()
        sns.barplot(x='population', y='ethnicity', data=ethnicity_dist, ax=ax)
        plt.title("Population Distribution by Ethnicity")
        plt.xlabel("Population")
        plt.ylabel("Ethnicity")
        st.pyplot(fig)

# Population trend over time, arranged below the above visualizations
st.write("### Population Trend Over Time")
if 'date' in filtered_data.columns and 'population' in filtered_data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    population_trend = filtered_data.groupby(filtered_data['date'].dt.year)['population'].sum()
    ax.plot(population_trend.index, population_trend.values, marker='o', linestyle='-')
    plt.title("Population Growth Trend in Malaysia")
    plt.xlabel("Year")
    plt.ylabel("Total Population")
    plt.grid(True)
    st.pyplot(fig)

# Additional insights
st.write("### Insights")
st.write("- Analyze how the population is distributed across different age groups, genders, and ethnicities.")
st.write("- Explore the population growth trends over time and identify patterns or anomalies.")
st.write("- Investigate the impact of different demographics on the overall population distribution.")
