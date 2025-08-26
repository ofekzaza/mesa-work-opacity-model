import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np

names = [
    "ours_interval_5",
    "ours_interval_10",
    "ours_interval_50",
    "mlt++",
    "supereduction_a=2",
    "normal",
    "ours_interval_3",
]
mass = 40

# Initialize figures for the 6 graph types
fig1, ax1 = plt.subplots()  # Opacity vs T
fig2, ax2 = plt.subplots()  # L vs L_Edd
fig3, ax3 = plt.subplots()  # Fluxes
fig4, ax4 = plt.subplots()  # Opacity vs Flux
fig5a, ax5a = plt.subplots()  # Central opacity vs time
fig5b, ax5b = plt.subplots()  # Surface L/Ledd vs time
fig6, ax6 = plt.subplots()  # Luminosity fractions

for name in names:
    path = f"{mass}m-{name}/LOGS"
    try:
        history = mr.MesaLogDir(path)
        prof = mr.MesaData(f"{path}/profile{history.profile_numbers[-1]}.data")

        # 1.2 Opacity vs Temperature
        # if "opacity" in prof.columns:
        # (line,) = ax1.plot(prof.logT, prof.opacity, label=name, linewidth=0.8)
        # # if "eff_opacity" in prof.columns:
        # ax1.plot(prof.logT, prof.eff_opacity, "--", color=line.get_color())

        # 2. Luminosity vs Eddington Luminosity
        # if "luminosity" in prof.columns and "opacity" in prof.columns:

        # ax2.plot(prof.mass, prof.luminosity, label=f"L {name}", linewidth=0.8)
        ax2.plot(prof.mass, prof.log_L_div_Ledd, "--", label=f"L_Edd {name}", linewidth=0.8)

        # 3. Radiative vs Eddington Flux
        # if "luminosity" in prof.columns and "radius" in prof.columns:
        r_cm = prof.radius * 6.957e10
        L_cgs = prof.luminosity * 3.828e33
        F_rad = L_cgs / (4 * np.pi * r_cm**2)
        F_edd = (2.998e10 * 6.6743e-8 * (prof.mass * 1.989e33)) / (r_cm**2 * prof.opacity)
        ax3.plot(r_cm / 6.957e10, F_rad, label=f"F_rad {name}", linewidth=0.8)
        ax3.plot(r_cm / 6.957e10, F_edd, "--", label=f"F_Edd {name}", linewidth=0.8)

        # 4. Opacity vs Flux
        # if "opacity" in prof.columns:
        r_cm = prof.radius * 6.957e10
        L_cgs = prof.luminosity * 3.828e33
        F_rad = L_cgs / (4 * np.pi * r_cm**2)
        ax4.scatter(prof.opacity, F_rad, s=5, label=name, alpha=0.6)

        # 5.1 Central Opacity vs Time
        # if "center_opacity" in history.columns:
        ax5a.plot(history.star_age, history.center_opacity, label=name, linewidth=0.8)

        # 5.2 Surface L/Ledd vs Time
        # if "log_L" in history.columns and "photosphere_opacity" in history.columns:
        M = mass * 1.989e33
        L = 10**history.log_L * 3.828e33
        kappa = history.photosphere_opacity
        Ledd_surface = 4 * np.pi * 6.6743e-8 * M * 2.998e10 / kappa
        ax5b.plot(history.star_age, L / Ledd_surface, label=name, linewidth=0.8)

        # 6. Luminosity Fractions
        # if "luminosity" in prof.columns and "conv_L" in prof.columns:
        L_tot = prof.luminosity[-1]
        ax6.plot(prof.mass, prof.luminosity / L_tot, label=f"Rad {name}", linewidth=0.8)
        ax6.plot(prof.mass, prof.conv_L / L_tot, "--", label=f"Conv {name}", linewidth=0.8)

    except FileNotFoundError:
        print(f"⚠️ Warning: {path} not found. Skipping.")

# -------------------------------
# Final formatting + save
# -------------------------------

# 1.2
ax1.set_xlabel(r"$\log T$ [K]")
ax1.set_ylabel(r"$\kappa$ [cm²/g]")
ax1.set_title("Opacity vs Temperature")
ax1.set_yscale("log"); ax1.grid(True); ax1.legend()
fig1.tight_layout(); fig1.savefig("1_opacity.png", dpi=300)

# 2
ax2.set_xlabel("Mass [$M_⊙$]")
ax2.set_ylabel("Luminosity [$L_⊙$]")
ax2.set_title("Luminosity vs Eddington Luminosity")
ax2.set_yscale("log"); ax2.grid(True); ax2.legend()
fig2.tight_layout(); fig2.savefig("2_L_vs_Ledd.png", dpi=300)

# 3
ax3.set_xlabel("Radius [$R_⊙$]")
ax3.set_ylabel("Flux [erg/s/cm²]")
ax3.set_title("Radiative vs Eddington Flux")
ax3.set_yscale("log"); ax3.grid(True); ax3.legend()
fig3.tight_layout(); fig3.savefig("3_flux.png", dpi=300)

# 4
ax4.set_xlabel(r"$\kappa$ [cm²/g]")
ax4.set_ylabel("F_rad [erg/s/cm²]")
ax4.set_title("Opacity vs Flux")
ax4.set_xscale("log"); ax4.set_yscale("log"); ax4.grid(True); ax4.legend()
fig4.tight_layout(); fig4.savefig("4_opacity_vs_flux.png", dpi=300)

# 5a
ax5a.set_xlabel("Age [yr]")
ax5a.set_ylabel(r"$\kappa_c$ [cm²/g]")
ax5a.set_title("Central Opacity vs Time")
ax5a.set_yscale("log"); ax5a.grid(True); ax5a.legend()
fig5a.tight_layout(); fig5a.savefig("5a_center_opacity.png", dpi=300)

# 5b
ax5b.set_xlabel("Age [yr]")
ax5b.set_ylabel(r"$L/L_{\rm Edd}$")
ax5b.set_title("Surface L/Ledd vs Time")
ax5b.set_yscale("log"); ax5b.grid(True); ax5b.legend()
fig5b.tight_layout(); fig5b.savefig("5b_L_over_Ledd.png", dpi=300)

# 6
ax6.set_xlabel("Mass [$M_⊙$]")
ax6.set_ylabel("Fraction of L")
ax6.set_title("Radiative vs Convective Luminosity Fractions")
ax6.grid(True); ax6.legend()
fig6.tight_layout(); fig6.savefig("6_luminosity_fractions.png", dpi=300)

plt.close("all")
