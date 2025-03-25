import matplotlib.pyplot as plt

# Data for the chart
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Create the line chart
plt.figure(figsize=(8, 5))  # Set the figure size
plt.plot(x, y, color='blue', marker='o', linestyle='-', linewidth=2, markersize=6, label='Line 1')

# Adding title and labels
plt.title("Example Line Chart", fontsize=14)
plt.xlabel("X-axis Label", fontsize=12)
plt.ylabel("Y-axis Label", fontsize=12)

# Add a grid
plt.grid(True, linestyle='--', alpha=0.6)

# Add a legend
plt.legend()

# Show the chart
plt.show()
