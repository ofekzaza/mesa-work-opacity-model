import mesa_reader as mr
import matplotlib.pyplot as plt

options = """

zone
mass
logR
logT
logRho
logP
x_mass_fraction_H
y_mass_fraction_He
z_mass_fraction_metals
extra_opacity_factor
dm
logdq
dq_ratio
q
vel_km_per_s
radius
radius_cm
logR_cm
rmid
velocity
v_div_r
pressure_scale_height
mmid
logxq
dr
log_dr
dr_div_cs
log_dr_div_cs
acoustic_depth
log_cell_collapse_time
temperature
energy
logE
rho
entropy
pressure
prad
pgas
logPgas
pgas_div_ptotal
eta
mu
grada
gamma1
free_e
csound
log_csound
v_div_csound
eps_grav
eps_nuc
non_nuc_neu
pp
cno
tri_alpha
c_alpha
n_alpha
o_alpha
ne_alpha
na_alpha
mg_alpha
si_alpha
s_alpha
ar_alpha
ca_alpha
ti_alpha
cr_alpha
fe_co_ni
c12_c12
c12_o16
o16_o16
pnhe4
photo
ni56_co56
co56_fe56
other
abar
zbar
z2bar
ye
x
y
z
log_z
h1
he3
he4
c12
n14
o16
ne20
mg24
si28
log_h1
log_he3
log_he4
log_c12
log_n14
log_o16
log_ne20
log_mg24
log_si28
opacity
log_opacity
log_kap_times_factor
luminosity
logL
log_L_div_Ledd
lum_adv
lum_conv
lum_erg_s
lum_plus_lum_adv
lum_rad
log_abs_lum_erg_s
total_energy
mlt_mixing_length
conv_vel
log_conv_vel
conv_L_div_L
log_conv_L_div_L
gradT
gradr
gradT_sub_grada
conv_vel_div_csound
log_mlt_D_mix
log_D_mix
log_D_conv
log_D_semi
log_D_ovr
log_D_thrm
log_D_minimum
log_D_rayleigh_taylor
log_D_omega
log_sig_mix
mix_type
tau
logtau
omega
log_omega
log_j_rot
log_J_div_M53
log_J_inside
log_abs_shear
i_rot
j_rot
v_rot
fp_rot
ft_rot
log_am_nu
r_polar
log_r_polar
r_equatorial
log_r_equatorial
r_e_div_r_p
omega_crit
omega_div_omega_crit
am_log_sig
am_log_D_DSI
am_log_D_SH
am_log_D_SSI
am_log_D_ES
am_log_D_GSF
am_log_D_ST
am_log_nu_ST
dynamo_log_B_r
dynamo_log_B_phi
RTI_du_diffusion_kick
alpha_RTI
boost_for_eta_RTI
dedt_RTI
dudt_RTI
eta_RTI
log_alpha_RTI
log_eta_RTI
log_lambda_RTI_div_Hrho
log_sig_RTI
log_source_minus_alpha_RTI
log_source_plus_alpha_RTI
lambda_RTI
v_div_v_escape
u
u_face
P_face
extra_heat
zFe
dPdr_dRhodr_info
dlogR
dPdr_info
dRhodr_info
log_du_kick_div_du
L_div_Ledd_effective
"""

mass = 30

y_axises = [
    "L_div_Ledd_effective",
    "log_L_div_Ledd",
    "log_opacity",
    "extra_opacity_factor",
    "logT",
    "entropy",
]

# List of history file names (without extensions)
names = [
    "normal",
    "ours_interval_3",
    "ours_interval_5",
    "ours_interval_10",
    "mlt++",
    "supereduction_a=2",
    # "ours_interval_50",
    # "supereduction_a=5",
]
y_axis = "L_div_Ledd_effective"
#'supereduction_a=5' empty it doesnt run
# Initialize the plot
def plot(x_axis: str, x_units: str, y_axis: str, y_units: str):
    plt.figure()

    # Iterate over each history file
    for name in names:
        path = f"{mass}m-{name}/LOGS"
        try:
            print(path)
            # Load the history data
            history = mr.MesaLogDir(path)
            # Plot log_L vs. log_Teff
            prof = mr.MesaData(f"{path}/profile{history.profile_numbers[-1]}.data")
            if (not hasattr(prof, y_axis)):
                raise ValueError(f"{y_axis} is not in prof")
            if (not hasattr(prof, x_axis)):
                raise ValueError(f"{x_axis} is not in prof")
            
            x_data = getattr(prof, x_axis)
            y_data = getattr(prof, y_axis)
            
            (line,) = plt.plot(x_data, y_data, "-", linewidth=0.8, label=name)
            color = line.get_color()
            plt.plot(x_data[-1], y_data[-1], "o", markersize=6, color=color)
            plt.plot(x_data[0], y_data[0], "o", markersize=6, color=color)

        except FileNotFoundError:
            print(f"Warning: {path}.data not found. Skipping.")

    # Customize the plot
    plt.xlabel(f"{x_axis} [{x_units}]")
    plt.ylabel(f"{y_axis} [{y_units}]")
    plt.title(f"Mass {mass}: {y_axis} vs {x_axis} at onset of Carbon burning")
    # plt.gca().invert_xaxis()  # HR diagrams have Teff decreasing to the right
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Save the plot
    plt.savefig(f"Mass_{mass}_{y_axis}_vs_{x_axis}.png", dpi=300)
    plt.close()

for y_axis in y_axises:
    print(y_axis)
    plot(x_axis="logRho", x_units="g/cm^3", y_axis=y_axis, y_units="")