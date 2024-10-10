import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Set up the Streamlit app title
st.title("Malaysian Population Data Dashboard 🇲🇾")

# Load the dataset
URL_DATA = 'https://storage.dosm.gov.my/population/population_malaysia.parquet'
df_malaysia = pd.read_parquet(URL_DATA)

# Convert 'date' column to datetime format
if 'date' in df_malaysia.columns:
    df_malaysia['date'] = pd.to_datetime(df_malaysia['date'])

# Clean and classify ethnicity
def classify_ethnicity(ethnicity):
    if ethnicity in ['overall']:
        return 'Overall'
    elif ethnicity in ['bumi', 'bumi_malay']:
        return 'Malay'
    elif ethnicity == 'chinese':
        return 'Chinese'
    elif ethnicity == 'indian':
        return 'Indian'
    elif ethnicity in ['other', 'bumi_other', 'other_citizen', 'other_noncitizen']:
        return 'Others'
    else:
        return 'Unknown'

df_malaysia['ethnicity'] = df_malaysia['ethnicity'].apply(classify_ethnicity)

# Clean and classify age groups
def classify_age_group(age):
    if age == 'overall':
        return 'Overall'
    age_ranges = {
        '18-24 (Gen Z)': ['15-19', '20-24'],
        '25-40 (Millennial)': ['25-29', '30-34', '35-39'],
        '41-56 (Gen X)': ['40-44', '45-49', '50-54', '55-59'],
        '57+ (Baby Boomers)': ['60-64', '65-69', '70+', '70-74', '75-79', '80+', '80-84', '85+']
    }
    for group, ranges in age_ranges.items():
        if age in ranges:
            return group
    return 'Unknown'

df_malaysia['age_group'] = df_malaysia['age'].apply(classify_age_group)

# Remove rows with 'Unknown' in ethnicity or age_group
df_malaysia = df_malaysia[(df_malaysia['ethnicity'] != 'Unknown') & (df_malaysia['age_group'] != 'Unknown')]

# Remove duplicate rows
df_malaysia = df_malaysia.drop_duplicates()

# Rename columns in the cleaned dataset
df_malaysia = df_malaysia.rename(columns={
    'date': 'Date',
    'sex': 'Gender',
    'age': 'Age',
    'age_group': 'Age_Group',
    'ethnicity': 'Ethnicity',
    'population': 'Sample_Population'
})

# Sidebar filters for interaction
st.sidebar.header("Filter the Data:")
sex_filter = st.sidebar.multiselect("Select Gender:", options=df_malaysia['Gender'].unique(), default=df_malaysia['Gender'].unique())
age_filter = st.sidebar.multiselect("Select Age Group:", options=df_malaysia['Age_Group'].unique(), default=df_malaysia['Age_Group'].unique())
ethnicity_filter = st.sidebar.multiselect("Select Ethnicity:", options=df_malaysia['Ethnicity'].unique(), default=df_malaysia['Ethnicity'].unique())
year_filter = st.sidebar.slider("Select Year Range:", int(df_malaysia['Date'].dt.year.min()), int(df_malaysia['Date'].dt.year.max()), (int(df_malaysia['Date'].dt.year.min()), int(df_malaysia['Date'].dt.year.max())))

# Filter the data based on selections
filtered_data = df_malaysia[
    (df_malaysia['Gender'].isin(sex_filter)) &
    (df_malaysia['Age_Group'].isin(age_filter)) &
    (df_malaysia['Ethnicity'].isin(ethnicity_filter)) &
    (df_malaysia['Date'].dt.year.between(year_filter[0], year_filter[1]))
]

# Display raw and filtered datasets side by side
st.write("### Dataset Comparison")
col1, col2, col3 = st.columns([3, 0.7, 3])

with col1:
    st.write("### Raw Dataset")
    st.write(df_malaysia)

with col2:
    # Create a placeholder to center the image vertically
    for _ in range(10):  # Adjust this range to increase/decrease vertical space
        st.text("")
    image = Image.open('assets/After_Cleaning.png')  # Load the uploaded image
    # Display the image
    st.image(image, use_column_width=True)

with col3:
    st.write("### Cleaned Dataset")
    st.write(filtered_data)

# Arrange visualizations in columns and rows
st.write("### Visualizations")

# Columns for population by age group and by ethnicity
col4, col5 = st.columns(2)

# Set a consistent figure size
fig_size = (8, 5)

# Population distribution by age group
with col4:
    if 'Age_Group' in filtered_data.columns and 'Sample_Population' in filtered_data.columns:
        st.subheader("Population Distribution by Age Group")
        fig, ax = plt.subplots(figsize=fig_size)
        sns.barplot(x='Age_Group', y='Sample_Population', data=filtered_data, hue='Gender', ax=ax)
        plt.xticks(rotation=45)
        plt.title("Population Distribution by Age Group")
        plt.xlabel("Age Group")
        plt.ylabel("Population")
        st.pyplot(fig)

# Population distribution by ethnicity
with col5:
    if 'Ethnicity' in filtered_data.columns and 'Sample_Population' in filtered_data.columns:
        st.subheader("Population Distribution by Ethnicity")
        fig, ax = plt.subplots(figsize=fig_size)
        ethnicity_dist = filtered_data.groupby('Ethnicity')['Sample_Population'].sum().reset_index()
        sns.barplot(x='Sample_Population', y='Ethnicity', data=ethnicity_dist, ax=ax)
        plt.title("Population Distribution by Ethnicity")
        plt.xlabel("Population")
        plt.ylabel("Ethnicity")
        st.pyplot(fig)

# Population trend over time, arranged below the above visualizations
st.write("### Population Trend Over Time")
if 'Date' in filtered_data.columns and 'Sample_Population' in filtered_data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    population_trend = filtered_data.groupby(filtered_data['Date'].dt.year)['Sample_Population'].sum()
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
