import streamlit as st
import pandas as pd

# Title for the app
st.title("CSV File Viewer and OFF Region Calculator")

# File uploader to browse and read CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Display the contents of the CSV file
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("**CSV Contents:**")
    st.dataframe(df)

# Numerical input fields for n1_L, n1_H, and H_1
n1_L = st.number_input('n1_L', min_value=0.0, value=0.0)
n1_H = st.number_input('n1_H', min_value=0.0, value=0.0)
H_1 = st.number_input('H_1', min_value=0.0, value=0.0)

# Calculate and display Lower OFF Region and Upper OFF Region
lower_off_region = n1_L + H_1
upper_off_region = n1_H - H_1

st.write(f"**Lower OFF Region:** {lower_off_region}")
st.write(f"**Upper OFF Region:** {upper_off_region}")
