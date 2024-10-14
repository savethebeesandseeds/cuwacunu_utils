import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore, Style, init


def plot_one_file(file_path, output_folder, output_filename):
    # Load the CSV file without headers
    try:
        df = pd.read_csv(file_path, header=None)
    except FileNotFoundError:
        print(f"{Fore.RED}✖ File not found: {file_path}")
        return
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Assign column names
    df.columns = [
        "Open time", "Open", "High", "Low", "Close", "Volume", 
        "Close time", "Quote asset volume", "Number of trades", 
        "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
    ]

    # Convert 'Open time' to datetime format
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')

    # Calculate Sell Volume
    df['Sell volume'] = df['Volume'] - df['Taker buy base asset volume']

    # Calculate the Volume Difference (Sell - Buy)
    df['Volume difference'] = df['Volume'] - 2 * df['Taker buy base asset volume']


    # Plot 1: Volume and Close Price vs Time (combined plot)
    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Volume', color=color)
    ax1.plot(df['Open time'], df['Volume'], linewidth=0.25, color=color, label='Total Volume')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # Create a second y-axis for the price data
    color = 'tab:green'
    ax2.set_ylabel('Close Price', color=color)
    ax2.plot(df['Open time'], df['Close'], linewidth=0.25, color=color, label='Close Price')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # Ensure labels don’t overlap
    plt.title('Volume and Close Price vs Time')
    plt.savefig(f"{output_folder}/volume-price-{output_filename}", bbox_inches='tight')

    # Plot 2: 
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot Total, Buy, and Sell Volumes on the first y-axis
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Volume')
    ax1.plot(df['Open time'], df['Volume'], linewidth=0.25, label='Total Volume', color='blue')
    ax1.plot(df['Open time'], df['Taker buy base asset volume'], linewidth=0.25, label='Buy Volume', color='green')
    ax1.plot(df['Open time'], df['Sell volume'], linewidth=0.25, label='Sell Volume', color='red')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # Create a second y-axis for the Volume Difference
    ax2 = ax1.twinx()
    ax2.set_ylabel('Volume Difference (Sell - Buy)', color='purple')
    ax2.plot(df['Open time'], df['Volume difference'], linewidth=0.25, label='Volume Difference', color='purple', linestyle='--')
    ax2.tick_params(axis='y', labelcolor='purple')

    # Plot the horizontal line y = 0 on the secondary y-axis
    ax2.axhline(y=0, color='black', linestyle=':', linewidth=1, label='y = 0')

    # Add title and adjust layout
    fig.suptitle('Total, Buy, Sell Volumes and Volume Difference vs Time')
    fig.tight_layout()
    plt.savefig(f"{output_folder}/volume-{output_filename}", bbox_inches='tight')

    # Plot 3: 
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_ylabel('Volume Difference (Sell - Buy)', color='purple')
    ax1.plot(df['Open time'], df['Volume difference'], linewidth=0.25, label='Volume Difference', color='purple', linestyle='--')
    ax1.tick_params(axis='y', labelcolor='purple')

    # Create a second y-axis for the Volume Difference
    color = 'tab:green'
    ax2 = ax1.twinx()
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Close Price', color=color)
    ax2.plot(df['Open time'], df['Close'], linewidth=0.25, color=color, label='Close Price')
    ax2.tick_params(axis='y', labelcolor=color)

    # Plot the horizontal line y = 0 on the secondary y-axis
    ax1.axhline(y=0, color='black', linestyle=':', linewidth=1, label='y = 0')

    fig.tight_layout()  # Ensure labels don’t overlap
    plt.title('Volume and Close Price vs Time')
    plt.savefig(f"{output_folder}/avg_volume-price-{output_filename}", bbox_inches='tight')
    plt.close(fig)


# Initialize colorama
init(autoreset=True)

# Global variables
symbols = ["BTCUSDT"]  # Add more symbols if needed
intervals = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w"]
years = ["2020", "2021", "2022", "2023", "2024"]  # Start from 2020 since earlier data might not exist
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

download_base_dir = "../data"  # Directory to store downloaded files
output_base_dir = "./output_dataviewer/"

# Example usage
if __name__ == "__main__":
    for symbol in symbols:
        for interval in intervals:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Vizualizing Symbol: {symbol}, Interval: {interval}")
            file_path = f'{download_base_dir}/{symbol}/{interval}/{symbol}-{interval}-all-years.csv'
            plot_one_file(file_path, f"{output_base_dir}/{symbol}/{interval}", f"{symbol}-{interval}-all-years.png")

            for year in years:
                print(f"{Fore.BLUE}  \tYear: {year}")
                file_path = f'{download_base_dir}/{symbol}/{interval}/{year}/{symbol}-{interval}-{year}.csv'
                plot_one_file(file_path, f"{output_base_dir}/{symbol}/{interval}/{year}/", f"{symbol}-{interval}-{year}.png")

                for month in months:
                    print(f"{Fore.YELLOW} \t\tMonth: {month}")
                    file_path = f'{download_base_dir}/{symbol}/{interval}/{year}/{month}/{symbol}-{interval}-{year}-{month}.csv'
                    plot_one_file(file_path, f"{output_base_dir}/{symbol}/{interval}/{year}/{month}", f"{symbol}-{interval}-{year}-{month}.png")

