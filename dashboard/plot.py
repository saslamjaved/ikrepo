# Re-importing required libraries due to environment reset
import matplotlib.pyplot as plt
import numpy as np

# Define the equations
# Equation 1: x + y = 1200 (rearranged to y = 1200 - x)
x_vals = np.linspace(0, 1200, 400)
y1 = 1200 - x_vals

# Equation 2: 60x + 100y = 88000 (rearranged to y = (88000 - 60x) / 100)
y2 = (88000 - 60 * x_vals) / 100

# Plot the equations
plt.figure(figsize=(10, 6))
plt.plot(x_vals, y1, label="x + y = 1200", color="blue")
plt.plot(x_vals, y2, label="60x + 100y = 88000", color="green")

# Intersection point calculation (solving equations manually or using code)
# From x + y = 1200 and 60x + 100y = 88000, solve for x and y.
# Substitute y = 1200 - x into 60x + 100y = 88000:
# 60x + 100(1200 - x) = 88000
# x = 800, y = 400
intersection_x, intersection_y = 800, 400

# Highlight the intersection point
plt.scatter(intersection_x, intersection_y, color="red", label="Intersection (800, 400)")

# Labels, legend, and grid
plt.title("Graphical Solution: Music Festival Tickets")
plt.xlabel("Number of $60 Tickets (x)")
plt.ylabel("Number of $100 Tickets (y)")
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.legend()
plt.show()