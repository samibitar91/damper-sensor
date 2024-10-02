import streamlit as st
import plotly.graph_objects as go

# Initialize session state for P1_H, H1 in Normal mode
if 'P1_H' not in st.session_state:
    st.session_state.P1_H = 0.5
if 'H1' not in st.session_state:
    st.session_state.H1 = 0.1

# Initialize session state for n1_H in Reversed mode
if 'n1_H' not in st.session_state:
    st.session_state.n1_H = 0.8

# Binary toggle for Normal or Reversed mode
output = st.radio("Select Output Mode", ('Normal', 'Reversed'))

if output == 'Normal':
    st.write("Normal Mode")

    # Slider for P1_L
    P1_L = st.slider("P1_L", min_value=0.0, max_value=1.0, step=0.001, format="%.3f")
    
    # Update the maximum value of P1_H to always be greater than P1_L
    st.session_state.P1_H = st.slider("P1_H", min_value=P1_L + 0.001, max_value=1.0, value=st.session_state.P1_H, step=0.001, format="%.3f")
    
    # Update H1 based on the current value of P1_H and P1_L
    max_H1 = min(P1_L, 1 - st.session_state.P1_H)
    st.session_state.H1 = st.slider("H1", min_value=0.0, max_value=(st.session_state.P1_H - P1_L), value=st.session_state.H1, step=0.001, format="%.3f")

    # Calculating Lower and Upper ON Regions
    Lower_ON = P1_L - st.session_state.H1
    Upper_ON = st.session_state.P1_H + st.session_state.H1

    # Display results
    st.write(f"Lower ON region: {Lower_ON}")
    st.write(f"Upper ON region: {Upper_ON}")

    # Plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[P1_L, P1_L], mode='lines', name='P1_L', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=[0, 1], y=[st.session_state.P1_H, st.session_state.P1_H], mode='lines', name='P1_H', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=[0, 1], y=[Lower_ON, Lower_ON], mode='lines', name='Lower ON Region', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=[0, 1], y=[Upper_ON, Upper_ON], mode='lines', name='Upper ON Region', line=dict(color='orange', dash='dash')))
    
    fig.update_layout(yaxis=dict(range=[0, 1]), title="ON Regions")
    
    st.plotly_chart(fig)

elif output == 'Reversed':
    st.write("Reversed Mode")

    # Sliders for n1_L and H1
    n1_L = st.slider('n1_L', 0.0, 1.0, 0.2, 0.001, format="%.3f")
    max_H1 = (1 - n1_L) / 2
    H1 = st.slider('H1', 0.0, max_H1, 0.05, 0.001, format="%.3f")

    # Update n1_H based on the current values of n1_L and H1
    st.session_state.n1_H = st.slider('n1_H', n1_L + 2*H1 + 0.001, 1.0, value=st.session_state.n1_H, step=0.001, format="%.3f")

    # Calculating Lower and Upper OFF Regions
    Lower_OFF = n1_L + H1
    Upper_OFF = st.session_state.n1_H - H1

    # Display results
    st.write(f"Lower OFF region: {Lower_OFF}")
    st.write(f"Upper OFF region: {Upper_OFF}")

    # Plot using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, 1], y=[n1_L, n1_L], mode='lines', name='n1_L', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=[0, 1], y=[st.session_state.n1_H, st.session_state.n1_H], mode='lines', name='n1_H', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=[0, 1], y=[Lower_OFF, Lower_OFF], mode='lines', name='Lower OFF Region', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=[0, 1], y=[Upper_OFF, Upper_OFF], mode='lines', name='Upper OFF Region', line=dict(color='orange', dash='dash')))

    fig.update_layout(yaxis=dict(range=[0, 1]), title="OFF Regions")

    st.plotly_chart(fig)
