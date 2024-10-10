import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from sklearn.linear_model import LinearRegression
import numpy as np

# Set up the Streamlit app title
st.title("Malaysian Population Data Dashboard 🇲🇾")

# Load the dataset
URL_DATA = 'https://storage.dosm.gov.my/population/population_malaysia.parquet'
df_raw = pd.read_parquet(URL_DATA)
df_malaysia = df_raw.copy()

# Convert 'date' column to datetime format
if 'date' in df_malaysia.columns:
    df_malaysia['date'] = pd.to_datetime(df_malaysia['date'], errors='coerce')

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

# Check for any NaT values after conversion
if df_malaysia['Date'].isna().any():
    st.warning("There are some NaT values in the Date column after conversion. Please check the data.")

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
col1, col2, col3 = st.columns([4, 1, 8])

with col1:
    st.write("### Raw Dataset")
    st.write(df_raw)

with col2:
    for _ in range(10):  # Adjust this range to increase/decrease vertical space
        st.text("")
    image = Image.open('assets/After_Cleaning.png')  # Load the uploaded image
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

# Population trend by age group and ethnicity arranged in columns
st.write("### Population Growth Trend by Age Group and Ethnicity")

# Create columns for the two graphs
col6, col7 = st.columns(2)

# Population trend by age group
with col6:
    st.subheader("Population Growth Trend by Age Group")
    if 'Date' in filtered_data.columns and 'Sample_Population' in filtered_data.columns:
        age_group_trend = filtered_data.groupby(['Date', 'Age_Group'])['Sample_Population'].sum().reset_index()
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=age_group_trend, x='Date', y='Sample_Population', hue='Age_Group', markers=True, dashes=False, ax=ax1)
        plt.title("Population Growth by Age Group")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(fig1)

# Population trend by ethnicity
with col7:
    st.subheader("Population Growth Trend by Ethnicity")
    if 'Date' in filtered_data.columns and 'Sample_Population' in filtered_data.columns:
        ethnicity_trend = filtered_data.groupby(['Date', 'Ethnicity'])['Sample_Population'].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.lineplot(data=ethnicity_trend, x='Date', y='Sample_Population', hue='Ethnicity', markers=True, dashes=False, ax=ax2)
        plt.title("Population Growth by Ethnicity")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(fig2)

# Prediction section
st.header("Predict Future Population Growth")

# Input fields for prediction
start_year = st.number_input("Select Start Year:", min_value=int(df_malaysia['Date'].dt.year.min()), max_value=2124, value=int(df_malaysia['Date'].dt.year.max()), step=1)
end_year = st.number_input("Select End Year:", min_value=start_year + 1, max_value=2124, value=start_year + 10, step=1)

# Multi-select for ethnicity and age group
selected_age_groups = st.multiselect("Select Age Groups for Prediction:", options=df_malaysia['Age_Group'].unique())
selected_ethnicities = st.multiselect("Select Ethnicities for Prediction:", options=df_malaysia['Ethnicity'].unique())

# Create columns for the two graphs
col8, col9 = st.columns(2)

# Predict future population for selected age groups
with col8:
    if selected_age_groups:  # Check if any age groups are selected
        # Prepare filtered data
        filtered_age_group_data = filtered_data[filtered_data['Age_Group'].isin(selected_age_groups)]
        
        # Prepare data for prediction
        X_age = filtered_age_group_data['Date'].dt.year.values.reshape(-1, 1)
        y_age = filtered_age_group_data['Sample_Population'].values

        # Train linear regression model
        model_age = LinearRegression()
        model_age.fit(X_age, y_age)

        # Predict future population
        future_years = np.arange(start_year, end_year + 1).reshape(-1, 1)
        predicted_population_age = model_age.predict(future_years)

        # Plot the prediction for age groups
        fig_age, ax_age = plt.subplots(figsize=(10, 6))
        
        # Plot historical data with labels for selected age groups
        for age_group in selected_age_groups:
            age_group_data = filtered_age_group_data[filtered_age_group_data['Age_Group'] == age_group]
            ax_age.plot(age_group_data['Date'].dt.year, age_group_data['Sample_Population'], marker='o', linestyle='-', label=f'Historical: {age_group}')
        
        # Plot predicted data
        ax_age.plot(future_years, predicted_population_age, label='Predicted Population', color='orange', marker='o', linestyle='--')
        
        plt.title(f"Population Growth Prediction for Selected Age Groups: {', '.join(selected_age_groups)}")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(fig_age)
    else:
        st.warning("Please select at least one Age Group for prediction.")

# Predict future population for selected ethnicities
with col9:
    if selected_ethnicities:  # Check if any ethnicities are selected
        # Prepare filtered data
        filtered_ethnicity_data = filtered_data[filtered_data['Ethnicity'].isin(selected_ethnicities)]
        
        # Prepare data for prediction
        X_ethnicity = filtered_ethnicity_data['Date'].dt.year.values.reshape(-1, 1)
        y_ethnicity = filtered_ethnicity_data['Sample_Population'].values

        # Train linear regression model
        model_ethnicity = LinearRegression()
        model_ethnicity.fit(X_ethnicity, y_ethnicity)

        # Predict future population
        future_years = np.arange(start_year, end_year + 1).reshape(-1, 1)
        predicted_population_ethnicity = model_ethnicity.predict(future_years)

        # Plot the prediction for ethnicities
        fig_ethnicity, ax_ethnicity = plt.subplots(figsize=(10, 6))
        
        # Plot historical data with labels for selected ethnicities
        for ethnicity in selected_ethnicities:
            ethnicity_data = filtered_ethnicity_data[filtered_ethnicity_data['Ethnicity'] == ethnicity]
            ax_ethnicity.plot(ethnicity_data['Date'].dt.year, ethnicity_data['Sample_Population'], marker='o', linestyle='-', label=f'Historical: {ethnicity}')

        # Plot predicted data
        ax_ethnicity.plot(future_years, predicted_population_ethnicity, label='Predicted Population', color='orange', marker='o', linestyle='--')
        
        plt.title(f"Population Growth Prediction for Selected Ethnicities: {', '.join(selected_ethnicities)}")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        st.pyplot(fig_ethnicity)
    else:
        st.warning("Please select at least one Ethnicity for prediction.")

# Footer for the app
st.write("### Data Source:")
st.write("[Department of Statistics Malaysia](https://www.dosm.gov.my/)")
