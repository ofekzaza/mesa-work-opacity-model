import mesa_reader as mr
import matplotlib.pyplot as plt

# List of history file names (without extensions)
names = [
    # "normal",
    # "ours_interval_2",
    # "ours_interval_3",
    # "ours_thermal_time",
    "ours_thermal_time",
        "ours_thermal_ofek",

    # "ours_interval_5",
    # "ours_interval_10",
    # "mlt++",
    # "supereduction_a=2",
    # "ours_interval_40",
    # "supereduction_a=5",
]
#'supereduction_a=5' empty it doesnt run
# Initialize the plot
plt.figure()

mass = 40


plt.figure()
for name in names:
    path = f"{mass}m-{name}/LOGS/history.data"
    
    try:
        # Load the history data
        history = mr.MesaData(path)
        # Plot log_L vs. log_Teff
        x = history.model_number
        kh = history.kh_timescale
        dt = history.time_step_sec / (3600 * 24 * 365)
        y = dt / kh
        (line,) = plt.plot(x, y, label=name, linewidth=0.8)
        color = line.get_color()
        plt.plot(x[-1], y[-1], "o", color=color)
    except FileNotFoundError:
        print(f"Warning: {path}.data not found. Skipping.")

# Customize the plot
plt.xlabel("model_number")
plt.ylabel("dt / kh_timescale")
plt.title(f"{mass} Mass Star dt / kh_timescale")
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig(f"Mass_{mass}_kh_dt.png", dpi=300)
plt.close()