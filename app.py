import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title for the app
st.title("Time Series Plot and OFF Region Calculation")

# Create two columns: inputs on the left, plot on the right
col1, col2 = st.columns([1, 3])

# File uploader in the left column
uploaded_file = col1.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Ensure the "Zeit" column is treated as the time axis (in seconds)
    if 'Zeit' in df.columns:
        df['Zeit'] = pd.to_numeric(df['Zeit'], errors='coerce')

    # Fill NaN or zero values in columns with linear interpolation
    df.replace(0, np.nan, inplace=True)  # Replace zeros with NaN to allow interpolation
    df.interpolate(method='linear', inplace=True)  # Perform linear interpolation

    # Display the cleaned dataframe in the left column
    col1.write("**Interpolated Time Series Data:**")
    col1.dataframe(df)

    # Numerical input sliders in the left column
    n1_L = col1.slider('n1_L', min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    n1_H = col1.slider('n1_H', min_value=0.0, max_value=100.0, value=50.0, step=0.1)
    H_1 = col1.slider('H_1', min_value=0.0, max_value=50.0, value=10.0, step=0.1)

    # Calculate Lower OFF Region and Upper OFF Region
    lower_off_region = n1_L + H_1
    upper_off_region = n1_H - H_1

    # Display OFF Region values in the left column
    col1.write(f"**Lower OFF Region:** {lower_off_region}")
    col1.write(f"**Upper OFF Region:** {upper_off_region}")

    # Plot the time series in the right column
    with col2:
        fig, ax = plt.subplots()

        # Plot each of the time series
        for column in ['Strg-Ein', 'Strg-Aus', 'Hebel']:
            if column in df.columns:
                ax.plot(df['Zeit'], df[column], label=column)

        # Add horizontal lines for OFF regions and input values
        ax.axhline(n1_L, color='blue', linestyle='--', label='n1_L')
        ax.axhline(n1_H, color='green', linestyle='--', label='n1_H')
        ax.axhline(lower_off_region, color='red', linestyle='--', label='Lower OFF Region')
        ax.axhline(upper_off_region, color='orange', linestyle='--', label='Upper OFF Region')

        # Labeling the plot
        ax.set_xlabel('Time (Seconds)')
        ax.set_ylabel('Values')
        ax.set_title('Time Series with OFF Region Lines')

        # Add legend
        ax.legend()

        # Display the plot
        st.pyplot(fig)
