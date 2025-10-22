import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_path = "./results_ad.csv"

# Read the CSV file
df = pd.read_csv(csv_path)

# Extract x and y data
x = df['value'].values
y = df['mean_time'].values

# Fit y = a*x (line through origin)
# The simplest way: a = sum(x*y) / sum(x*x)
a = np.sum(x * y) / np.sum(x * x)

print(f"Fitted parameter: a = {a:.6f}")
print(f"This means: mean_time ≈ {a:.6f} × value")

# Create visualization
plt.figure(figsize=(10, 6))

# Plot original data points with error bars
plt.errorbar(x, y, yerr=df['std_time'], 
             fmt='o', capsize=5, capthick=2, markersize=8,
             label='Measured Data', color='blue', alpha=0.7)

# Plot fitted line
x_fit = np.linspace(0, x.max() * 1.1, 100)
y_fit = a * x_fit
plt.plot(x_fit, y_fit, 'r-', linewidth=2, 
         label=f'Fit: y = {a:.4f}x')

# Labels and formatting
plt.xlabel('Value', fontsize=12)
plt.ylabel('Mean Time', fontsize=12)
plt.title('Linear Fit: y = a×x', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

# Save the plot
plt.tight_layout()
plt.savefig('./linear_fit.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved!")

# Calculate fit quality (R-squared)
y_pred = a * x
residuals = y - y_pred
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y - np.mean(y))**2)
r_squared = 1 - (ss_res / ss_tot)

print(f"\nFit Quality (R²): {r_squared:.4f}")
