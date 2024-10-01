import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title for the app
st.title("Time Series Plot and OFF Region Calculation")

# File uploader to browse and read CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the semicolon-separated CSV file into a DataFrame
    df = pd.read_csv(uploaded_file, sep=';')

    # Ensure the "Zeit" column is treated as the time axis (in seconds)
    if 'Zeit' in df.columns:
        df['Zeit'] = pd.to_numeric(df['Zeit'], errors='coerce')

    # Convert all other columns to numeric, ignoring errors
    for column in df.columns:
        if column != 'Zeit':  # We already converted 'Zeit'
            df[column] = pd.to_numeric(df[column], errors='coerce')

    # Fill NaN or zero values in columns with linear interpolation
    df.replace(0, np.nan, inplace=True)  # Replace zeros with NaN to allow interpolation
    df.interpolate(method='linear', inplace=True)  # Perform linear interpolation

    # Display the cleaned dataframe
    st.write("**Interpolated Time Series Data:**")
    st.dataframe(df)

    # Numerical input sliders with 3 decimal place precision
    n1_L = st.slider('n1_L', min_value=0.001, max_value=1.0, value=0.001, step=0.001, format="%.3f")
    
    # n1_H slider: displayed limits are 0 to 1, but it can't go below n1_L
    n1_H = st.slider('n1_H', min_value=n1_L, max_value=1.0, value=n1_L, step=0.001, format="%.3f")

    # Calculate the maximum allowed value for H_1 based on n1_L and n1_H
    max_H1 = min(n1_H - n1_L, (n1_H - n1_L) / 2)

    # H_1 slider: displayed limits are 0 to 1, but it can't go below 0 and is constrained by max_H1
    H_1 = st.slider('H_1', min_value=0.0, max_value=max_H1, value=0.0, step=0.001, format="%.3f")

    # Calculate Lower OFF Region and Upper OFF Region
    lower_off_region = n1_L + H_1
    upper_off_region = n1_H - H_1

    # Display OFF Region values
    st.write(f"**Lower OFF Region:** {lower_off_region}")
    st.write(f"**Upper OFF Region:** {upper_off_region}")

    # Plot the time series
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
