import math
import os
import json
import numpy as np
import mesa_reader as mr
import matplotlib.pyplot as plt


def plot(mass: int, model_var: str, y_axis: str, y_units: str, value_axis: str):
    """
    model_var: the field holding model number (always 'model_number')
    y_axis: the vertical axis variable (e.g. 'logRho')
    value_axis: the heatmap color variable (e.g. 'extra_opacity_factor')
    """

    # name = "ours_thermal_time4"
    # name = "ours_thermal_time_by_thermal_kh"
    name = "ours copy"
    # name = "ours_interval_3"
    path = f"{mass}m-{name}/LOGS"

    print(f"Reading profiles from: {path}")

    profiles = []

    # Read all profiles and collect model numbers
    model_numbers = []
    star_ages = []
    Y_all = []
    VAL_all = []

    for i in range(1, 9999):
        f_path = f"{path}/profile{i}.data"
        if not os.path.exists(f_path):
            break

        prof = mr.MesaData(f_path)

        # Ensure required fields exist
        if not hasattr(prof, y_axis) or not hasattr(prof, value_axis):
            print(f"Profile {i} missing required fields, skipping.")
            continue

        profiles.append(f_path)
        model_numbers.append(getattr(prof, "model_number"))
        star_ages.append(getattr(prof, "star_age"))

        Y_all.append(np.array(getattr(prof, y_axis), dtype=float))
        VAL_all.append(np.array(getattr(prof, value_axis), dtype=float))

    if not profiles:
        raise FileNotFoundError("No profiles found.")

    # Build common y-grid (vertical axis)
    min_y = min(np.min(arr) for arr in Y_all)
    max_y = max(np.max(arr) for arr in Y_all)
    n_points = max(len(arr) for arr in Y_all)

    common_y = np.linspace(min_y, max_y, n_points)

    # Heatmap matrix
    n_models = len(model_numbers)
    DATA = np.zeros((n_points, n_models))

    # Fill the heatmap interpolating each profile
    for j in range(n_models):
        y_data = Y_all[j]
        val_data = VAL_all[j]

        # Interpolate to common y grid
        interp_val = np.interp(common_y, y_data, val_data)
        DATA[:, j] = interp_val

    # Save raw matrix for debugging
    with open("tmp.json", "w") as f:
        json.dump(DATA.tolist(), f)

    # Sort by model number (important!)
    model_numbers = np.array(model_numbers)
    star_ages = np.array(star_ages)
    sort_idx = np.argsort(model_numbers)

    DATA = DATA[:, sort_idx]
    model_numbers = model_numbers[sort_idx]
    star_ages = star_ages[sort_idx]

    # Plot heatmap
    plt.figure(figsize=(10, 6))
    plt.imshow(
        DATA,
        cmap="viridis",
        origin="lower",
        aspect="auto",
        vmax=1,
        vmin=math.floor(np.min(DATA) * 100) / 100,
        extent=[model_numbers[0], model_numbers[-1], common_y[0], common_y[-1]],
    )

    plt.colorbar(label=f"{value_axis}")

    # Update x-axis labels to include star_age
    ax = plt.gca()
    # Get current ticks (auto-selected by matplotlib based on extent)
    # We force a draw to make sure ticks are populated, though usually get_xticks works if we use the current axes
    xticks = ax.get_xticks()

    # Filter xticks to those within valid range
    xticks = [x for x in xticks if model_numbers[0] <= x <= model_numbers[-1]]

    new_labels = []
    for x in xticks:
        # Interpolate to find age for this model number
        # We can use np.interp because model_numbers are sorted
        age = np.interp(x, model_numbers, star_ages)
        new_labels.append(f"{int(x)}\n{age:.2e}")

    ax.set_xticks(xticks)
    ax.set_xticklabels(new_labels)

    plt.xlabel("Model Number\n(Star Age [years])")
    plt.ylabel(f"{y_axis} [{y_units}]")
    plt.title(f"{value_axis} vs {y_axis} across Model Number")

    plt.tight_layout()
    plt.savefig(f"HEATMAP_{mass}_{name}_{value_axis}_vs_{y_axis}.png", dpi=300)
    plt.close()


# RUN
for mass in [40]:
    plot(
        mass=mass,
        model_var="model_number",
        y_axis="logRho",
        y_units="g/cm^3",
        value_axis="extra_opacity_factor",
    )
