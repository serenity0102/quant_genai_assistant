import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import boto3

# Read the CSV file from s3
s3 = boto3.client('s3', 'ap-east-1')
obj = s3.get_object(Bucket='bucket4jackysharinghk', Key='cpi.txt.csv')
df = pd.read_csv(obj['Body'])

# Convert Month to datetime
df['Month'] = pd.to_datetime(df['Month'], format='%y-%b')

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot both CPI lines
ax.plot(df['Month'], df['China-CPI'], marker='o', label='China CPI')
ax.plot(df['Month'], df['US-CPI'], marker='o', label='US CPI')

# Customize the plot
plt.title('China vs US CPI Comparison')
plt.xlabel('Month')
plt.ylabel('CPI Value')
plt.grid(True)
plt.legend()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)

# Display the data table
st.write("CPI Data:")
st.dataframe(df)


