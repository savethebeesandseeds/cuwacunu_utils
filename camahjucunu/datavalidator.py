import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Style, init

def detect_inconsistent_intervals(df, time_column):
    """
    Detect missing or inconsistent intervals in a Unix timestamp series.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing the time series data.
    time_column (str): Name of the column with Unix timestamps.
    
    Returns:
    pd.DataFrame: DataFrame with interval deltas and inconsistency flags.
    """
    # Step 1: Sort the DataFrame by the time column
    df = df.sort_values(by=time_column).reset_index(drop=True)

    df['Time Human']  = pd.to_datetime(df[time_column], unit='ms')
    # Step 2: Calculate differences between consecutive timestamps
    df['Time Delta'] = df[time_column].diff()
    df['Price Delta'] = df['Open'].shift(-1) - df['Close']

    # Step 3: Detect the most common interval (mode)
    common_interval = df['Time Delta'].mode()[0]
    print("\t\tCommon interval: ", common_interval)

    df['Delta units'] = df['Time Delta'] / common_interval

    # Step 4: Create a boolean flag for inconsistencies
    df['Inconsistent'] = df['Time Delta'] != common_interval

    # Step 5: Return the DataFrame with deltas and inconsistency flags
    return df


def plot_triple_axis(df, output_folder, output_filename):
    """
    Plot time deltas, inconsistencies, and price delta on three axes,
    with thin lines at y=0 and vertical connections from the line to the points.

    Parameters:
    df (pd.DataFrame): DataFrame containing the deltas and inconsistency flags.
    output_folder (str): Folder where the plot will be saved.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set values to NaN where 'Inconsistent' is False to avoid plotting them
    delta_units_filtered = df['Delta units'].where(df['Inconsistent'] == 1, np.nan)
    price_delta_filtered = df['Price Delta'].where(df['Inconsistent'] == 1, np.nan)
    inconsistent_filtered = df['Inconsistent'].where(df['Inconsistent'] == 1, np.nan)

    # Increase the figure size to make space for the third axis
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Primary y-axis (Delta units)
    ax1.axhline(y=0, color='b', linewidth=0.5, linestyle='--')  # Thin blue line at y=0
    ax1.vlines(df.index, ymin=0, ymax=delta_units_filtered, color='b', linewidth=0.5)  # Vertical lines
    ax1.plot(df.index, delta_units_filtered, marker='o', linestyle='-', color='b', label='Delta units')
    ax1.set_xlabel('Index')
    ax1.set_ylabel('Delta units', color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True)

    # Secondary y-axis (Inconsistent)
    ax2 = ax1.twinx()
    ax2.axhline(y=0, color='r', linewidth=0.5, linestyle='--')  # Thin red line at y=0
    ax2.vlines(df.index, ymin=0, ymax=inconsistent_filtered, color='r', linewidth=0.5)  # Vertical lines
    ax2.plot(df.index, inconsistent_filtered, marker='x', linestyle='--', color='r', linewidth=0.25, label='Inconsistent')
    ax2.set_ylabel('Inconsistent (1=True)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Tertiary y-axis (Price Delta)
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 80))  # Further offset the third axis
    ax3.axhline(y=0, color='g', linewidth=0.5, linestyle='--')  # Thin green line at y=0
    ax3.vlines(df.index, ymin=0, ymax=price_delta_filtered, color='g', linewidth=0.5)  # Vertical lines
    ax3.plot(df.index, price_delta_filtered, marker='^', linestyle='-', linewidth=0.25, color='g', label='Price Delta')
    ax3.set_ylabel('Price Delta', color='g')
    ax3.tick_params(axis='y', labelcolor='g')

    # Adjust layout to prevent overlapping of labels and legends
    fig.tight_layout()
    fig.subplots_adjust(right=0.75)  # Make space for the third axis

    # Add title and legends
    fig.suptitle(f'Delta units, Inconsistency Detection, and Price Delta: {output_filename}', y=1.02)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax3.legend(loc='center right', bbox_to_anchor=(1.25, 0.5))  # Adjust legend to fit

    # Save and close the plot
    plt.savefig(f"{output_folder}/{output_filename}", bbox_inches='tight')
    plt.close(fig)



def validate_single_file(file_path, output_path, output_filename):
    # Load the CSV file without headers
    try:
        df = pd.read_csv(file_path, header=None)
    except FileNotFoundError:
        print(f"{Fore.RED}✖ File not found: {file_path}")
        return

    # Assign column names
    df.columns = [
        "Open time", "Open", "High", "Low", "Close", "Volume", 
        "Close time", "Quote asset volume", "Number of trades", 
        "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
    ]

    # Detect inconsistencies
    df_with_deltas = detect_inconsistent_intervals(df, 'Open time')

    # Find inconsistencies
    inconsistencies = df_with_deltas[df_with_deltas['Inconsistent']]

    # Display the result
    print(f"{Fore.CYAN}\t\tValidating filepath: {Fore.YELLOW}{output_filename}")
    
    if inconsistencies.shape[0]> 1:
        print(f"{Fore.RED}{Style.BRIGHT}⚠ \t\tInconsistent Intervals Found:")
        # print(inconsistencies.to_string(index=False))
        print(f"{Fore.GREEN}\t\tPlotting the time deltas...\n")
        plot_triple_axis(df_with_deltas, output_path, output_filename)
    else:
        print(f"{Fore.GREEN}✔ \t\tAll intervals are consistent.\n")

# Initialize colorama
init(autoreset=True)

# Global variables
symbols = ["BTCUSDT"]  # Add more symbols if needed
intervals = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w"]
years = ["2020", "2021", "2022", "2023", "2024"]  # Start from 2020 since earlier data might not exist
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

download_base_dir = "../data"  # Directory to store downloaded files
output_base_dir = "./output_validator/"

# Example usage
if __name__ == "__main__":
    for symbol in symbols:
        for interval in intervals:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Processing Symbol: {symbol}, Interval: {interval}")
            file_path = f'{download_base_dir}/{symbol}/{interval}/{symbol}-{interval}-all-years.csv'
            validate_single_file(file_path, f"{output_base_dir}/{symbol}/{interval}", f"{symbol}-{interval}-all-years.png")

            for year in years:
                print(f"{Fore.BLUE}  \tYear: {year}")
                file_path = f'{download_base_dir}/{symbol}/{interval}/{year}/{symbol}-{interval}-{year}.csv'
                validate_single_file(file_path, f"{output_base_dir}/{symbol}/{interval}/{year}/", f"{symbol}-{interval}-{year}.png")

                for month in months:
                    print(f"{Fore.YELLOW} \t\tMonth: {month}")
                    file_path = f'{download_base_dir}/{symbol}/{interval}/{year}/{month}/{symbol}-{interval}-{year}-{month}.csv'
                    validate_single_file(file_path, f"{output_base_dir}/{symbol}/{interval}/{year}/{month}", f"{symbol}-{interval}-{year}-{month}.png")

