import numpy as np

# Variable units: rho (kg/m^3), Vp (km/s), Vs (km/s)
radius, _, _, density, vp, vs = np.loadtxt("V5-Th.out", skiprows=1).T

# Find layer boundaries for each model based on jumps in values
# Only do this for the first (density), then share with other values
diffs = abs(vs[:-1] - vs[1:])

for i in [1, 2, 3, 4]:
    bigval = np.sort(diffs)[-i]
    big_idx = np.where(np.isin(diffs, bigval))[0]
    rad = (radius[big_idx], big_idx)
    print(rad)
    if i == 1:
        CoreMantB = rad[0]
    if i == 2:
        CrustantB = rad[0]
    if i == 3:
        UpMantLowMantB = rad[0]
    if i == 4:
        DownMantB = rad[0]
print(CoreMantB, UpMantLowMantB, CrustantB, DownMantB)

output = open("model_layers.txt", "w")
for i, rad in enumerate(radius):
    rad = float(rad)*1000
    if i == 0:
        output.write('  radius_ak135(  1) =  0.000000000000000E+000\n')
    if 100 < rad < 1000:
        if len(str(i+2)) == 1:
            output.write(f"  radius_ak135(  {i+2}) =   {rad:.10f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  radius_ak135( {i+2}) =   {rad:.10f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  radius_ak135({i+2}) =   {rad:.10f}\n")
    elif rad > 1000:
        if len(str(i+2)) == 1:
            output.write(f"  radius_ak135(  {i+2}) =   {rad:.9f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  radius_ak135( {i+2}) =   {rad:.9f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  radius_ak135({i+2}) =   {rad:.9f}\n") 
    elif rad < 100:
        if len(str(i+2)) == 1:
            output.write(f"  radius_ak135(  {i+2}) =   {rad:.11f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  radius_ak135( {i+2}) =   {rad:.11f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  radius_ak135({i+2}) =   {rad:.11f}\n")

output.write("\n")
for i, den in enumerate(density):
    dens =  float(den/1000)
    if dens < 10:
        if i == 0:
            output.write(f'  density_ak135(  1) =   {dens:.14f}\n')
        if len(str(i+2)) == 1:
            output.write(f"  density_ak135(  {i+2}) =   {dens:.14f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  density_ak135( {i+2}) =   {dens:.14f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  density_ak135({i+2}) =   {dens:.14f}\n")
    elif dens >= 10:
        if i == 0:
            output.write(f'  density_ak135(  1) =   {dens:.13f}\n')
        if len(str(i+2)) == 1:
            output.write(f"  density_ak135(  {i+2}) =   {dens:.13f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  density_ak135( {i+2}) =   {dens:.13f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  density_ak135({i+2}) =   {dens:.13f}\n")

output.write("\n")
for i, vel_p in enumerate(vp):
    vel_p = float(vel_p)
    if vel_p < 10:
        if i == 0:
            output.write(f'  vp_ak135(  1) =   {vel_p:.14f}\n')
        if len(str(i+2)) == 1:
            output.write(f"  vp_ak135(  {i+2}) =   {vel_p:.14f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  vp_ak135( {i+2}) =   {vel_p:.14f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  vp_ak135({i+2}) =   {vel_p:.14f}\n")
    elif vel_p >= 10:
        if i == 0:
            output.write(f'  vp_ak135(  1) =   {vel_p:.13f}\n')
        if len(str(i+2)) == 1:
            output.write(f"  vp_ak135(  {i+2}) =   {vel_p:.13f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  vp_ak135( {i+2}) =   {vel_p:.13f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  vp_ak135({i+2}) =   {vel_p:.13f}\n")

output.write("\n")
for i, vel_s in enumerate(vs):
    vel_s = float(vel_s)
    if i == 0:
        output.write(f'  vs_ak135(  {i+1}) =  0.000000000000000E+000\n')
    if int(vel_s) == 0:
        if len(str(i+2)) == 1:
            output.write(f'  vs_ak135(  {i+2}) =  0.000000000000000E+000\n')
        elif len(str(i+2)) == 2:    
            output.write(f'  vs_ak135( {i+2}) =  0.000000000000000E+000\n')
        elif len(str(i+2)) == 3:
            output.write(f'  vs_ak135({i+2}) =  0.000000000000000E+000\n')
    else:
        if len(str(i+2)) == 1:
            output.write(f"  vs_ak135(  {i+2}) =   {vel_s:.14f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  vs_ak135( {i+2}) =   {vel_s:.14f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  vs_ak135({i+2}) =   {vel_s:.14f}\n")

output.write("\n")
for i, rad in enumerate(radius):

    if rad <= CoreMantB:
        qkappa = 57822.0
        if i == 0:
            output.write(f'  Qkappa_ak135(  1) =   {qkappa:.12f}\n')
        if len(str(i+2)) == 1:
            output.write(f"  Qkappa_ak135(  {i+2}) =   {qkappa:.12f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  Qkappa_ak135( {i+2}) =   {qkappa:.12f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  Qkappa_ak135({i+2}) =   {qkappa:.12f}\n")

    elif rad <= UpMantLowMantB:

        qkappa = 1085.40170213
        if len(str(i+2)) == 1:
            output.write(f"  Qkappa_ak135(  {i+2}) =   {qkappa:.13f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  Qkappa_ak135( {i+2}) =   {qkappa:.13f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  Qkappa_ak135({i+2}) =   {qkappa:.13f}\n")

    elif rad <= CrustantB:
        qkappa = 328.05937500
        if len(str(i+2)) == 1:
            output.write(f"  Qkappa_ak135(  {i+2}) =   {qkappa:.14f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  Qkappa_ak135( {i+2}) =   {qkappa:.14f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  Qkappa_ak135({i+2}) =   {qkappa:.14f}\n")

    elif rad > CrustantB:
        qkappa = 1170.39500000
        if len(str(i+2)) == 1:
            output.write(f"  Qkappa_ak135(  {i+2}) =   {qkappa:.13f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  Qkappa_ak135( {i+2}) =   {qkappa:.13f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  Qkappa_ak135({i+2}) =   {qkappa:.13f}\n")

output.write("\n")
for i, rad in enumerate(radius):
    if rad <= CoreMantB:
        if i == 0:
            output.write(f'  Qmu_ak135(  {i+1}) =  0.000000000000000E+000\n')
        if len(str(i+2)) == 1:
            output.write(f'  Qmu_ak135(  {i+2}) =  0.000000000000000E+000\n')
        elif len(str(i+2)) == 2:    
            output.write(f'  Qmu_ak135( {i+2}) =  0.000000000000000E+000\n')
        elif len(str(i+2)) == 3:
            output.write(f'  Qmu_ak135({i+2}) =  0.000000000000000E+000\n')
    elif rad <= UpMantLowMantB:
        qmu = 430.81553191
        if len(str(i+2)) == 1:
            output.write(f"  Qmu_ak135(  {i+2}) =   {qmu:.14f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  Qmu_ak135( {i+2}) =   {qmu:.14f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  Qmu_ak135({i+2}) =   {qmu:.14f}\n")

    elif rad <= CrustantB:
        qmu = 130.54500000
        if len(str(i+2)) == 1:
            output.write(f"  Qmu_ak135(  {i+2}) =   {qmu:.14f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  Qmu_ak135( {i+2}) =   {qmu:.14f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  Qmu_ak135({i+2}) =   {qmu:.14f}\n")

    elif rad > CrustantB:
        qmu = 501.96000000
        if len(str(i+2)) == 1:
            output.write(f"  Qmu_ak135(  {i+2}) =   {qmu:.14f}\n")
        elif len(str(i+2)) == 2:
            output.write(f"  Qmu_ak135( {i+2}) =   {qmu:.14f}\n")
        elif len(str(i+2)) == 3:
            output.write(f"  Qmu_ak135({i+2}) =   {qmu:.14f}\n")
output.close()

