import mesa_reader as mr
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
import os


def plot_hr_diagram():
    # Model configuration based on the reference image and user request
    models = [
        {
            "name": "30m-normal",
            "label": "Default",
            "color": "violet",
            "linestyle": "--",
            "path": "30m-normal/LOGS",
        },
        {
            "name": "30m-mlt++",
            "label": "MLT++",
            "color": "darkorange",
            "linestyle": "-",
            "path": "30m-mlt++/LOGS",
        },
        {
            "name": "30m-ours_interval_3",
            "label": r"$\alpha_1 = \alpha_2 = 5$",
            "color": "tab:blue",
            "linestyle": "-",
            "path": "30m-ours_interval_3/LOGS",
        },
        {
            "name": "30m-supereduction_a=2",
            "label": r"$\alpha_1 = \alpha_2 = 2$",
            "color": "darkviolet",
            "linestyle": ":",
            "linewidth": 2,  # Make dotted line more visible
            "path": "30m-supereduction_a=2/LOGS",
        },
    ]

    fig, ax = plt.subplots(figsize=(10, 8))

    # Pre-load data to avoid re-reading for insets
    loaded_data = []
    for model in models:
        history_path = os.path.join(model["path"], "history.data")
        if not os.path.exists(history_path):
            print(
                f"Warning: History file not found for {model['name']} at {history_path}"
            )
            loaded_data.append(None)
            continue

        print(f"Loading {model['name']}...")
        h = mr.MesaData(history_path)
        loaded_data.append(h)

    # Helper function to plot on a given axis
    def plot_on_axis(axis, linewidth_scale=1.0):
        for i, model in enumerate(models):
            h = loaded_data[i]
            if h is None:
                continue

            axis.plot(
                h.log_Teff,
                h.log_L,
                label=model["label"] if axis == ax else "",
                color=model["color"],
                linestyle=model["linestyle"],
                linewidth=model.get("linewidth", 1.5) * linewidth_scale,
            )

    # Main plot
    plot_on_axis(ax)

    # Styling Main Plot
    ax.set_xlabel(r"$\log(T_{\rm eff}/\rm{K})$", fontsize=14)
    ax.set_ylabel(r"$\log(L/\rm{L}_\odot)$", fontsize=14)

    # Set explicit limits as requested by user based on image
    ax.set_xlim(5.5, 3.4)  # Inverted x-axis
    ax.set_ylim(5.1, 5.75)

    ax.legend(
        fontsize=12,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        ncol=2,
        frameon=False,
    )
    ax.tick_params(
        axis="both", which="major", labelsize=12, direction="in", top=True, right=True
    )
    ax.tick_params(axis="both", which="minor", direction="in", top=True, right=True)

    # --- Inset 1: Blue Loop / TAMS region (Left side) ---
    # Zoom factor: 3.5 (slightly higher zoom for focus)
    # Location: Center Left
    axins1 = zoomed_inset_axes(
        ax,
        zoom=3.5,
        loc="center left",
        bbox_to_anchor=(0.12, 0.45),
        bbox_transform=ax.transAxes,
    )
    plot_on_axis(axins1)

    # Limits for TAMS/Blue loop wiggle
    # Trying to capture the "hooks"
    x1, x2 = 4.8, 4.5
    y1, y2 = 5.3, 5.5
    axins1.set_xlim(x1, x2)
    axins1.set_ylim(y1, y2)

    # Fix ticks on inset
    axins1.invert_xaxis()  # Important to maintain direction
    axins1.tick_params(axis="both", which="both", labelsize=10, direction="in")
    axins1.set_xticks([])
    axins1.set_yticks([])

    mark_inset(ax, axins1, loc1=2, loc2=4, fc="none", ec="0.5")

    # --- Inset 2: Red Supergiant Tip (Right side) ---
    # Zoom factor: 3.5
    # Location: Bottom right quadrant usually, matches "lower right" of main flow but placed to the right
    axins2 = zoomed_inset_axes(
        ax,
        zoom=3.5,
        loc="lower right",
        bbox_to_anchor=(0.93, 0.25),
        bbox_transform=ax.transAxes,
    )
    plot_on_axis(axins2)

    # Limits for RSG tip
    # Focusing on the end of the red tracks
    x3, x4 = 3.8, 3.6
    y3, y4 = 5.2, 5.5
    axins2.set_xlim(x3, x4)
    axins2.set_ylim(y3, y4)

    # Fix ticks on inset
    axins2.invert_xaxis()
    axins2.tick_params(axis="both", which="both", labelsize=10, direction="in")
    axins2.set_xticks([])
    axins2.set_yticks([])

    mark_inset(ax, axins2, loc1=1, loc2=3, fc="none", ec="0.5")

    plt.tight_layout()

    output_file = "hr_diagram_comparison_30m.png"
    plt.savefig(output_file, dpi=300)
    print(f"Plot saved to {output_file}")
    plt.close()


if __name__ == "__main__":
    plot_hr_diagram()
