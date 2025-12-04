# Weather Data Visualizer - Complete Python Code

# -------------------------------
# Task 1: Import Libraries
# -------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Task 2: Data Acquisition & Loading
# -------------------------------
# Load the dataset
df = pd.read_csv('weather_data.csv')

# Inspect the dataset
print("Dataset Head:\n", df.head())
print("\nDataset Info:\n", df.info())
print("\nDataset Description:\n", df.describe())

# -------------------------------
# Task 3: Data Cleaning & Processing
# -------------------------------
# Handle missing values (drop rows with NaNs)
df = df.dropna()

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter relevant columns
df = df[['Date', 'Temperature', 'Rainfall', 'Humidity']]

# -------------------------------
# Task 4: Statistical Analysis
# -------------------------------
# Daily stats
daily_mean = np.mean(df['Temperature'])
daily_min = np.min(df['Temperature'])
daily_max = np.max(df['Temperature'])
daily_std = np.std(df['Temperature'])

print(f"\nDaily Temperature Stats - Mean: {daily_mean:.2f}, Min: {daily_min}, Max: {daily_max}, Std: {daily_std:.2f}")

# Monthly stats
monthly_stats = df.resample('M', on='Date').agg({'Temperature': ['mean','min','max','std'],
                                                 'Rainfall': 'sum',
                                                 'Humidity': 'mean'})
print("\nMonthly Stats:\n", monthly_stats)

# Yearly stats
yearly_stats = df.resample('Y', on='Date').agg({'Temperature': ['mean','min','max','std'],
                                                'Rainfall': 'sum',
                                                'Humidity': 'mean'})
print("\nYearly Stats:\n", yearly_stats)

# -------------------------------
# Task 5: Visualization
# -------------------------------
plt.style.use('seaborn-darkgrid')  # nicer plot style

# Line chart - Daily Temperature Trend
plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Temperature'], color='red')
plt.title('Daily Temperature Trend')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.savefig('temperature_trend.png')
plt.show()

# Bar chart - Monthly Rainfall
monthly_rainfall = df.resample('M', on='Date')['Rainfall'].sum()
plt.figure(figsize=(12,5))
monthly_rainfall.plot(kind='bar', color='blue')
plt.title('Monthly Rainfall')
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.savefig('monthly_rainfall.png')
plt.show()

# Scatter plot - Humidity vs Temperature
plt.figure(figsize=(8,5))
plt.scatter(df['Humidity'], df['Temperature'], color='green')
plt.title('Humidity vs Temperature')
plt.xlabel('Humidity (%)')
plt.ylabel('Temperature (°C)')
plt.savefig('humidity_vs_temperature.png')
plt.show()

# Combined plot - Temperature and Rainfall
fig, ax = plt.subplots(2, 1, figsize=(12,10))
ax[0].plot(df['Date'], df['Temperature'], color='red')
ax[0].set_title('Daily Temperature Trend')
ax[0].set_ylabel('Temperature (°C)')

ax[1].bar(monthly_rainfall.index, monthly_rainfall.values, color='blue')
ax[1].set_title('Monthly Rainfall')
ax[1].set_ylabel('Rainfall (mm)')

plt.tight_layout()
plt.savefig('combined_plot.png')
plt.show()

# -------------------------------
# Task 6: Grouping & Aggregation
# -------------------------------
# Group by month
monthly_avg_temp = df.groupby(df['Date'].dt.month)['Temperature'].mean()
monthly_total_rainfall = df.groupby(df['Date'].dt.month)['Rainfall'].sum()
monthly_avg_humidity = df.groupby(df['Date'].dt.month)['Humidity'].mean()

print("\nMonthly Aggregated Stats:\n")
print(pd.DataFrame({
    'Avg_Temperature': monthly_avg_temp,
    'Total_Rainfall': monthly_total_rainfall,
    'Avg_Humidity': monthly_avg_humidity
}))

# Optional: Group by season
def month_to_season(month):
    if month in [12,1,2]:
        return 'Winter'
    elif month in [3,4,5]:
        return 'Spring'
    elif month in [6,7,8]:
        return 'Summer'
    else:
        return 'Autumn'

df['Season'] = df['Date'].dt.month.apply(month_to_season)
seasonal_stats = df.groupby('Season').agg({'Temperature':'mean', 'Rainfall':'sum', 'Humidity':'mean'})
print("\nSeasonal Stats:\n", seasonal_stats)

# -------------------------------
# Task 7: Export Cleaned Data & Plots
# -------------------------------
# Export cleaned dataset
df.to_csv('cleaned_weather_data.csv', index=False)
print("\nCleaned dataset exported as 'cleaned_weather_data.csv'.")

# Plots already saved during plotting steps

# -------------------------------
# Task 8: Reporting (Markdown or text report)
# -------------------------------
report = """
Weather Data Analysis Report
============================

Dataset Overview:
- Columns: Date, Temperature, Rainfall, Humidity
- Records: {}

Data Cleaning:
- Missing values dropped
- Date column converted to datetime

Key Insights:
- Highest average temperature: {:.2f} °C
- Lowest temperature: {:.2f} °C
- Month with highest rainfall: {}
- Season with highest average humidity: {}

Visualizations:
- temperature_trend.png
- monthly_rainfall.png
- humidity_vs_temperature.png
- combined_plot.png
""".format(len(df), daily_mean, daily_min,
           monthly_total_rainfall.idxmax(), 
           seasonal_stats['Humidity'].idxmax())

with open('report.txt', 'w') as f:
    f.write(report)

print("\nReport saved as 'report.txt'.")
