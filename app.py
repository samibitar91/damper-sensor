import streamlit as st
import matplotlib.pyplot as plt

# Binary toggle for Normal or Reversed mode
output = st.radio("Select Output Mode", ('Normal', 'Reversed'))

if output == 'Normal':
    st.write("Normal Mode")

    # Sliders for P1_L, P1_H, H1
    P1_L = st.slider("P1_L", min_value=0.0, max_value=1.0, step=0.001, format="%.3f")
    max_H1 = min(P1_L, 1 - P1_H)
    P1_H = st.slider("P1_H", min_value=P1_L, max_value=1.0, step=0.001, format="%.3f")
    H1 = st.slider("H1", min_value=0.0, max_value=(P1_H - P1_L), step=0.001, format="%.3f")



    # Calculating Lower and Upper ON Regions
    Lower_ON = P1_L - H1
    Upper_ON = P1_H + H1

    # Display results
    st.write(f"Lower ON region: {Lower_ON}")
    st.write(f"Upper ON region: {Upper_ON}")

    # Plot the horizontal lines
    fig, ax = plt.subplots()
    ax.axhline(P1_L, color='blue', label='P1_L')
    ax.axhline(P1_H, color='green', label='P1_H')
    ax.axhline(Lower_ON, color='red', linestyle='--', label='Lower ON Region')
    ax.axhline(Upper_ON, color='orange', linestyle='--', label='Upper ON Region')
    ax.legend()

    st.pyplot(fig)

elif output == 'Reversed':
    st.write("Reversed Mode")

    # Sliders for n1_L, n1_H, H1
    n1_L = st.slider('n1_L', 0.0, 1.0, 0.2, 0.001, format="%.3f")
    max_H1 = (1 - n1_L) / 2
    H1 = st.slider('H1', 0.0, max_H1, 0.05, 0.001, format="%.3f")
    n1_H = st.slider('n1_H', n1_L + 2*H1, 1.0, 0.8, 0.001, format="%.3f")

    # Calculating Lower and Upper OFF Regions
    Lower_OFF = n1_L + H1
    Upper_OFF = n1_H - H1

    # Display results
    st.write(f"Lower OFF region: {Lower_OFF}")
    st.write(f"Upper OFF region: {Upper_OFF}")

    # Plot the horizontal lines
    fig, ax = plt.subplots()
    ax.axhline(n1_L, color='blue', label='n1_L')
    ax.axhline(n1_H, color='green', label='n1_H')
    ax.axhline(Lower_OFF, color='red', linestyle='--', label='Lower OFF Region')
    ax.axhline(Upper_OFF, color='orange', linestyle='--', label='Upper OFF Region')
    ax.legend()

    st.pyplot(fig)
