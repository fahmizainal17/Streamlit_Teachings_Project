import streamlit as st
import pandas as pd
from component import page_style

page_style()

# Title and Introduction
st.title("Analytics Dashboard 📊")

st.write("Hi there 👋. Welcome to our dashboard! In this web app, we will explore the ideas of how to use the Streamlit framework to create a Proof of Concept (POC).")

st.write("We will start with a simple example of displaying text, and then gradually explore more examples of different types of widgets and visualizations to create a simple analytics dashboard.")

st.write("Let's start with our first example!")

# Example 1: Display a DataFrame
st.subheader("Example 1: Displaying a Simple DataFrame")

# Create a simple DataFrame
data = {
    'Name': ['John', 'Anna', 'Peter', 'Linda'],
    'Age': [28, 24, 35, 32],
    'Department': ['Sales', 'Marketing', 'Finance', 'HR']
}

df = pd.DataFrame(data)

# Display the DataFrame
st.write("Here’s a simple DataFrame:")
st.dataframe(df)

# Example 2: Interactive Widget - User Input
st.subheader("Example 2: User Input")

name = st.text_input("Enter your name:")
if name:
    st.write(f"Hello, {name}! 👋")

# Example 3: Slider Widget for Data Exploration
st.subheader("Example 3: Age Filter")

age_filter = st.slider("Select age range:", min_value=20, max_value=40, value=(20, 35))
filtered_df = df[(df['Age'] >= age_filter[0]) & (df['Age'] <= age_filter[1])]

st.write("Filtered DataFrame based on age range:")
st.dataframe(filtered_df)

# Example 4: Visualization
st.subheader("Example 4: Visualization")

# Add a sample bar chart
st.bar_chart(df['Age'])

st.write("This is a simple bar chart visualizing the ages of people in our DataFrame.")

# Example 5: Upload a File
st.subheader("Example 5: File Upload")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    st.write("Here’s the uploaded DataFrame:")
    st.dataframe(uploaded_df)

# Example 6: Button Interaction
st.subheader("Example 6: Button Interaction")

if st.button("Click me"):
    st.write("Button clicked! 🎉")

# Final Remarks
st.write("That's all for now! 🎈In the next page , we will deep dive into some of the examples of dashboard namely Continents Population Data and US Airport Traffic")
