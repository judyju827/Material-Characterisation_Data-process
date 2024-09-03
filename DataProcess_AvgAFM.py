# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 12:38:48 2024

@author: judit
"""

import pandas as pd
import matplotlib.pyplot as plt

# List of file paths for your 5 datasets
file_paths = [
    r'C:\Users\judit\OneDrive - Imperial College London\MSE Yr2\UROPs\Materials\Judy AFM\Dataset4\Data1.xyz',
    r'C:\Users\judit\OneDrive - Imperial College London\MSE Yr2\UROPs\Materials\Judy AFM\Dataset4\Data3.xyz',
    r'C:\Users\judit\OneDrive - Imperial College London\MSE Yr2\UROPs\Materials\Judy AFM\Dataset4\Data3.xyz',
    r'C:\Users\judit\OneDrive - Imperial College London\MSE Yr2\UROPs\Materials\Judy AFM\Dataset4\Data4.xyz',
    r'C:\Users\judit\OneDrive - Imperial College London\MSE Yr2\UROPs\Materials\Judy AFM\Dataset4\Data5.xyz'
]

# Initialize a DataFrame to store the sum of Z values for averaging later
aggregated_data = None

for file_path in file_paths:
    # Load the CSV data
    data = pd.read_csv(file_path, delim_whitespace=True, header=None, names=['X', 'Y', 'Z'])
    
    # Group the data by y-axis values and calculate the average z-value for each y
    profile_data_y = data.groupby('Y')['Z'].mean().reset_index()
    
    # Initialize aggregated_data if it's the first file, otherwise add to it
    if aggregated_data is None:
        aggregated_data = profile_data_y
    else:
        aggregated_data['Z'] += profile_data_y['Z']

# Average the Z values by dividing by the number of datasets
aggregated_data['Z'] /= len(file_paths)

# Detect peaks in the averaged profile data
peak_threshold = 0.000000007 # This threshold might need adjustment
aggregated_data['Z_diff'] = aggregated_data['Z'].diff().abs()

# Identify the peaks by finding points where the difference exceeds the threshold
peak_indices = aggregated_data[aggregated_data['Z_diff'] > peak_threshold].index

if not peak_indices.empty:
    peak_range_y_min = aggregated_data.loc[peak_indices.min(), 'Y']
    peak_range_y_max = aggregated_data.loc[peak_indices.max(), 'Y']

    # Calculate average height for irradiated and unirradiated regions excluding peaks
    irradiated_region = aggregated_data[aggregated_data['Y'] < peak_range_y_min]
    unirradiated_region = aggregated_data[aggregated_data['Y'] > peak_range_y_max]

    # Calculate average heights excluding peaks
    avg_irradiated_height = irradiated_region['Z'].mean()
    avg_unirradiated_height = unirradiated_region['Z'].mean()

    # Create a 2D plot for the y-axis vs. height (z-axis)
    plt.figure(figsize=(10, 6))
    plt.plot(aggregated_data['Y'], aggregated_data['Z'], label='Average Height Profile', color='blue')

    # Highlight the peak region with a shaded area
    plt.axvspan(peak_range_y_min, peak_range_y_max, color='blue', alpha=0.3, label='Peak Region')

    # Plot average height lines for specific regions
    plt.hlines(y=avg_irradiated_height, xmin=aggregated_data['Y'].min(), xmax=peak_range_y_min, color='red', linestyle='--', label='Avg Irradiated Height')
    plt.hlines(y=avg_unirradiated_height, xmin=peak_range_y_max, xmax=aggregated_data['Y'].max(), color='blue', linestyle='--', label='Avg Unirradiated Height')

    # Adding labels and title
    plt.xlabel('Position (y-axis)')
    plt.ylabel('Height (z-axis)')
    plt.title('Averaged Height Profile Across Datasets')
    plt.legend()

    plt.grid(False)
    plt.show()

    print(f"Average Irradiated Height (Excluding Peaks): {avg_irradiated_height*1e6} um")
    print(f"Average Unirradiated Height (Excluding Peaks): {avg_unirradiated_height*1e6} um")


else:
    print("No significant peaks detected with the given threshold.")
