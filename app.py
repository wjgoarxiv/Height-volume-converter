import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

# Function to calculate volume from height
def volume_from_height(height, slope, intercept):
    return slope * height + intercept

# Data from the tables provided
data = {
    'trial1': {'volume': [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160],
               'height': [2.7, 3.2, 3.6, 3.9, 4.3, 4.6, 4.9, 5.3, 5.7, 6.1, 6.5, 6.8]},
    'trial2': {'volume': [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160],
               'height': [2.7, 3.2, 3.6, 3.9, 4.3, 4.6, 4.9, 5.3, 5.7, 5.9, 6.3, 6.7]},
    'trial3': {'volume': [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160],
               'height': [2.7, 3.2, 3.5, 3.8, 4.1, 4.5, 4.9, 5.2, 5.6, 6.0, 6.3, 6.7]}
}

# Convert the data into Pandas DataFrames
df1 = pd.DataFrame(data['trial1'])
df2 = pd.DataFrame(data['trial2'])
df3 = pd.DataFrame(data['trial3'])

# Calculate the mean and standard deviation of the height at each volume
mean_height = pd.concat([df1['height'], df2['height'], df3['height']], axis=1).mean(axis=1)
std_height = pd.concat([df1['height'], df2['height'], df3['height']], axis=1).std(axis=1)

# Linear regression to find the slope and intercept
slope, intercept, r_value, p_value, std_err = stats.linregress(mean_height, df1['volume'])

# Streamlit UI
st.title('Linear Fit Analysis (Height vs Volume)')

## Description
st.markdown("""
            높이 (cm)를 입력하면, 그에 따른 용량 (mL)을 계산해주는 앱입니다. \n
            피팅 정보는 사이드바를 확인하세요. :smile:
            """)

# Main page for input
input_height = st.number_input("Enter the height (cm):", min_value=0.0, value=2.7, step=0.1, max_value=7.0) # 반응기 계면 보이는 구간 (2.7 ~ 6.7)

# Calculate volume using the input height
calculated_volume = volume_from_height(input_height, slope, intercept)
st.write(f"Calculated volume: {calculated_volume:.3f} mL")

# Sidebar for plot and equation
with st.sidebar:
    st.header('Linear Fit Plot')

    # Plot the data and linear fit
    fig, ax = plt.subplots()
    ax.errorbar(mean_height, df1['volume'], xerr=std_height, fmt='o', ecolor='black', capsize=5, label='Measurements', color='black', alpha=0.9, linewidth=2)
    heights_for_line = np.linspace(min(mean_height), max(mean_height), 100)
    ax.plot(heights_for_line, volume_from_height(heights_for_line, slope, intercept), 'black', label='Linear Fit', alpha=0.7, linewidth=1, linestyle='-.')
    ax.set_xlabel('Height (cm)')
    ax.set_ylabel('Volume (mL)')
    ax.set_title('Linear fitting')
    ax.legend()
    ax.grid(True)
    
    # Display plot in Streamlit sidebar
    st.pyplot(fig)

    # Equation and function parameters in the sidebar
    st.header('Function Parameters')
    st.write(f"Volume = {slope:.3f} * Height + {intercept:.3f}")
    st.write(f"r = {r_value:.3f}")
    st.write(f"std_err = {std_err:.3f}")
    st.write(f"R_squared = {r_value**2:.3f}")

    # Table info.
    st.header("Tables for the data")
    st.write("Trial 1")
    st.write(df1)
    st.write("Trial 2")
    st.write(df2)
    st.write("Trial 3")
    st.write(df3)
