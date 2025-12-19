import mesa_reader as mr
import matplotlib.pyplot as plt
import os

# List of history file names (without extensions)
names = [
    # "normal",
    # "ours_interval_2",
    # "ours_interval_3",
    # "ours_thermal_time",
    # "ours_interval_5",
    # "ours_interval_10",
    "normal",
    "ours",
    "mlt++",
    "supereduction_a=2",
    # "ours_interval_40",
    "supereduction_a=5",
]
#'supereduction_a=5' empty it doesnt run
# Initialize the plot
plt.figure()

mass = 30

# Iterate over each history file
for name in names:
    path = f"{mass}m-{name}/LOGS/history.data"
    try:
        # Load the history data
        history = mr.MesaData(path)
        # Plot log_L vs. log_Teff
        (line,) = plt.plot(history.log_Teff, history.log_L, label=name, linewidth=0.8)
        color = line.get_color()
        plt.plot(history.log_Teff[-1], history.log_L[-1], "o", color=color)
    except FileNotFoundError:
        print(f"Warning: {path}.data not found. Skipping.")

# Customize the plot
plt.xlabel("log(Teff) [K]")
plt.ylabel("log(Luminosity / L☉)")
plt.title(f"{mass} Mass Star Hertzsprung-Russell Diagram")
plt.gca().invert_xaxis()  # HR diagrams have Teff decreasing to the right
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot
os.makedirs(f"plot{mass}m", exist_ok=True)
plt.savefig(f"plot{mass}m/mass_{mass}_hr_diagram_comparison.png", dpi=300)
plt.close()
