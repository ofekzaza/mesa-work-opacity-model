import mesa_reader as mr
import matplotlib.pyplot as plt

# List of history file names (without extensions)
names = ['ours_interval_5','ours_interval_10','ours_interval_50', 'mlt++', 'supereduction_a=2', 'normal']
#'supereduction_a=5' empty it doesnt run
# Initialize the plot
plt.figure()

mass = 40

# Iterate over each history file
for name in names:
    path = f'{mass}m-{name}/LOGS'
    try:
        # Load the history data
        history = mr.MesaLogDir(path)
        # Plot log_L vs. log_Teff
        prof = mr.MesaData(f"{path}/profile{history.profile_numbers[-1]}.data")
        line, = plt.plot(prof.logRho, prof.logT, '-', linewidth=0.8, label=name)
        color = line.get_color()
        plt.plot(prof.logRho[-1], prof.logT[-1], 'o', markersize=6, color=color)
    except FileNotFoundError:
        print(f"Warning: {path}.data not found. Skipping.")

# Customize the plot
plt.xlabel(r'$\log(\rho)\ \,[\mathrm{g/cm^3}]$')
plt.ylabel(r'$\log(T)\ \,[\mathrm{K}]$')
plt.title("mass {mass}: Temperature vs Density at onset of Carbon burning")
#plt.gca().invert_xaxis()  # HR diagrams have Teff decreasing to the right
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig('Temperature vs Density .png', dpi=300)
plt.close()

