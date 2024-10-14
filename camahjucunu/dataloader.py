import numpy as np
import matplotlib.pyplot as plt

def softmax(x):
    # Subtract the max value from each element for numerical stability
    exps = np.exp(x - np.max(x))
    return exps / np.sum(exps, axis=0)

def cumulative_time_encoding(timesteps):
    """
    Generate a cumulative time encoding for the given number of timesteps.
    Args:
        timesteps (int): Number of time steps (e.g., 96).
    Returns:
        np.array: Cumulative encoding of shape (timesteps,).
    """
    # Initialize the encoding with a base value for each interval
    encoding = np.zeros(timesteps)

    # Define ranges for different time groups
    encoding[:60] = np.log(1)  # Seconds (1 to 60)
    encoding[60:75] = np.log(1*60)  # Minutes (60+)
    encoding[75:79] = np.log(1*60*15)  # 15-minute intervals
    encoding[79:85] = np.log(1*60*60)  # Hour intervals
    encoding[85:89] = np.log(1*60*60*6)  # 6-hour intervals
    encoding[89:] = np.log(1*60*60*24)  # Day intervals

    # # Normalize by the total seconds in a day (1 * 60 * 60 * 24)
    encoding /= np.log(1 * 60 * 60 * 24)

    # # Define ranges for different time groups
    # encoding[:60] = (1)  # Seconds (1 to 60)
    # encoding[60:75] = (1*60)  # Minutes (60+)
    # encoding[75:79] = (1*60*15)  # 15-minute intervals
    # encoding[79:85] = (1*60*60)  # Hour intervals
    # encoding[85:89] = (1*60*60*6)  # 6-hour intervals
    # encoding[89:] = (1*60*60*24)  # Day intervals

    # # # Normalize by the total seconds in a day (1 * 60 * 60 * 24)
    # encoding /= (1 * 60 * 60 * 24)

    return encoding

# Generate cumulative time encoding
timesteps = 96
time_enc = cumulative_time_encoding(timesteps)

# Create a sample input tensor (random data for two features)
np.random.seed(42)
input_tensor = np.random.random((1, timesteps, 2))

# Apply cumulative time encoding to the input tensor (broadcasting)
encoded_tensor = input_tensor + time_enc[:, np.newaxis]

# Plotting: Before and After Encoding, and Cumulative Time Encoding Values
fig, axs = plt.subplots(3, 2, figsize=(15, 10))

for i in range(2):  # Iterate over two features
    # Input Tensor (Before Encoding)
    axs[0, i].plot(input_tensor[0, :, i], label=f"Feature {i+1} (Input)", color='tab:blue')
    axs[0, i].set_title(f"Feature {i+1} - Input Tensor")
    axs[0, i].legend()

    # Cumulative Time Encoding
    axs[1, i].plot(time_enc, label=f"Feature {i+1} (Encoding)", color='tab:green')
    axs[1, i].set_title(f"Feature {i+1} - Cumulative Time Encoding")
    axs[1, i].legend()

    # Encoded Tensor (After Adding Cumulative Encoding)
    axs[2, i].plot(encoded_tensor[0, :, i], label=f"Feature {i+1} (Encoded)", color='tab:red')
    axs[2, i].set_title(f"Feature {i+1} - Encoded Tensor")
    axs[2, i].legend()

# Adjust layout and show plot
plt.tight_layout()
plt.savefig("waka.png")
