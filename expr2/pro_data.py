import pandas as pd
import matplotlib.pyplot as plt

csv_path = "./results_ad.csv"

# Read the CSV file
df = pd.read_csv(csv_path)

# Create a simple figure
plt.figure(figsize=(10, 6))

# Plot mean_time with error bars (using std_time as the error)
plt.errorbar(df['value'], df['mean_time'], yerr=df['std_time'], 
             marker='o', linestyle='-', capsize=5, capthick=2,
             markersize=8, linewidth=2, label='Mean Time')

# Add labels and title
plt.xlabel('Value', fontsize=12)
plt.ylabel('Time', fontsize=12)
plt.title('Mean Time vs Value (with Standard Deviation)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Save the plot
plt.tight_layout()
plt.savefig('./timing_visualization.png', dpi=300, bbox_inches='tight')
print("Visualization saved!")

print(df.describe())
