# Weather Data Visualizer - <Your Name>

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# -----------------------------
# Configurations
# -----------------------------
DATA_FILE = "data/weather_data.csv"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# 1. Load & Clean Data
# -----------------------------
df = pd.read_csv(DATA_FILE)

# Handle missing values
df = df.dropna(subset=['Date', 'Temperature', 'Rainfall', 'Humidity'])

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Keep relevant columns
df = df[['Date', 'Temperature', 'Rainfall', 'Humidity']]

# Save cleaned data
cleaned_file = os.path.join(OUTPUT_DIR, "cleaned_weather_data.csv")
df.to_csv(cleaned_file, index=False)

# -----------------------------
# 2. Statistical Analysis
# -----------------------------
# Daily statistics
daily_stats = df.describe()

# Monthly aggregation
df['Month'] = df['Date'].dt.month
monthly_stats = df.groupby('Month').agg({
    'Temperature': 'mean',
    'Rainfall': 'sum',
    'Humidity': 'mean'
})

# Yearly aggregation
df['Year'] = df['Date'].dt.year
yearly_stats = df.groupby('Year').agg({
    'Temperature': 'mean',
    'Rainfall': 'sum',
    'Humidity': 'mean'
})

# Seasonal mapping
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df['Season'] = df['Month'].apply(get_season)
seasonal_stats = df.groupby('Season').agg({
    'Temperature': 'mean',
    'Rainfall': 'sum',
    'Humidity': 'mean'
})

# -----------------------------
# 3. Visualizations
# -----------------------------
# Line chart: Daily temperature trend
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Temperature'], color='orange')
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "temperature_trend.png"))
plt.close()

# Bar chart: Monthly rainfall totals
plt.figure(figsize=(8, 5))
plt.bar(monthly_stats.index, monthly_stats['Rainfall'], color='blue')
plt.title("Monthly Rainfall Totals")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "monthly_rainfall.png"))
plt.close()

# Scatter plot: Humidity vs Temperature
plt.figure(figsize=(8, 5))
plt.scatter(df['Temperature'], df['Humidity'], color='green', alpha=0.5)
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "humidity_vs_temperature.png"))
plt.close()

# Combined plot: Temperature and Rainfall
fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(df['Date'], df['Temperature'], color='red', label='Temperature (°C)')
ax1.set_xlabel('Date')
ax1.set_ylabel('Temperature (°C)', color='red')
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.bar(df['Date'], df['Rainfall'], color='blue', alpha=0.3, label='Rainfall (mm)')
ax2.set_ylabel('Rainfall (mm)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

fig.tight_layout()
plt.title("Temperature and Rainfall Over Time")
plt.savefig(os.path.join(OUTPUT_DIR, "temperature_rainfall_combined.png"))
plt.close()

# -----------------------------
# 4. Generate Summary Report
# -----------------------------
report_file = os.path.join(OUTPUT_DIR, "report.txt")
with open(report_file, 'w') as f:
    f.write("Weather Data Visualizer Report\n")
    f.write("============================\n\n")
    
    f.write("Daily Statistics:\n")
    f.write(daily_stats.to_string())
    f.write("\n\nMonthly Statistics:\n")
    f.write(monthly_stats.to_string())
    f.write("\n\nYearly Statistics:\n")
    f.write(yearly_stats.to_string())
    f.write("\n\nSeasonal Statistics:\n")
    f.write(seasonal_stats.to_string())

print(f"All outputs saved in '{OUTPUT_DIR}' folder.")
