import numpy as np

model = "V1-Tc"
fid = model + ".out"
radius, temperature, pressure, density, vp, vs = np.loadtxt(fid, skiprows=1).T
# km, K, GPa, kg/m^3, km/s, km/s
max_radius = radius.max()
depth = max_radius - radius

# Convert density from kg/m^3 to g/cm^3
density = density / 1000.0
new_file = model + ".tvel"

depth = depth[::-1]
vp = vp[::-1]
vs = vs[::-1]
density = density[::-1]

# Create .tvel file with fixed format
with open(new_file, "w") as f:
    f.write(model + " - P\n")
    f.write(model + " - S\n")
    for i in range(len(radius)):
        f.write(f"{depth[i]:10.4f} {vp[i]:10.4f} {vs[i]:10.4f} {density[i]:10.4f}\n")
f.close()