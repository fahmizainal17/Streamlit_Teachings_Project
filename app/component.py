import streamlit as st
from PIL import Image

def page_style():
    custom_style = """
    <style>
        body {
            background-color: #f0f0f5;  /* Light gray background for the body */
            color: #333;  /* Dark gray text color */
            font-family: 'Arial', sans-serif;  /* Font style for the text */
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;  /* White background for the sidebar */
            padding: 20px;  /* Padding for the sidebar */
            border-radius: 10px;  /* Rounded corners for the sidebar */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* Subtle shadow for depth */
        }
        h1, h2, h3 {
            font-weight: bold;  /* Bold headings */
            color: #4CAF50;  /* Green color for headings */
        }
        button {
            background-color: #4CAF50;  /* Green button background */
            color: white;  /* White text for buttons */
            border: none;  /* No border for buttons */
            padding: 10px 20px;  /* Button padding */
            text-align: center;  /* Centered text */
            font-size: 16px;  /* Button font size */
            margin: 4px 2px;  /* Margin for buttons */
            cursor: pointer;  /* Pointer cursor on hover */
            border-radius: 8px;  /* Rounded corners for buttons */
            transition: background-color 0.3s;  /* Smooth background color transition */
        }
        button:hover {
            background-color: #45a049;  /* Darker green on hover */
        }
    </style>
    """

    # Set the page configuration
    icon = Image.open('photos/My_Photo/Round_Profile_Photo.jpg')
    st.set_page_config(page_title="Fahmi Zainal", page_icon=icon, layout="wide")

    # Apply custom styles to the page
    st.markdown(custom_style, unsafe_allow_html=True)

    # Display the main background image
    image = Image.open('photos/My_Photo/Background_Photo.png')
    st.image(image)

    with st.sidebar:
        # Sidebar Title
        st.title("About Me")
        
        # Display Profile Picture
        profile_pic = Image.open('photos/My_Photo/Round_Profile_Photo.jpg')  # Replace with your image path
        st.image(profile_pic, width=150)  # Display the profile picture with a width of 150px

        # Add a brief description
        st.write("""
        Hi! I'm Fahmi Zainal, a passionate learner in the field of artificial intelligence and business administration. 
        I'm excited to share my projects and connect with others in the community!
        """)

        # Add links to social media or other resources
        st.subheader("Connect with Me")
        st.markdown("""
        - [LinkedIn](https://www.linkedin.com/in/your-linkedin-profile)  <!-- Replace with your actual LinkedIn URL -->
        - [GitHub](https://github.com/your-github-profile)  <!-- Replace with your actual GitHub URL -->
        """)

        # Music button
        st.markdown(new_tab_button, unsafe_allow_html=True)

        # Add a section for additional resources or interests
        st.subheader("Interests")
        st.write("""
        - Machine Learning
        - Web Development
        - Data Visualization
        """)

        # Add a button to open your portfolio
        st.markdown("""
        <a href="https://your-portfolio-link.com" target="_blank">
            <button>
                View My Portfolio
            </button>
        </a>
        """, unsafe_allow_html=True)
