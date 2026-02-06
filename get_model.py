import numpy as np

equal_spacing = False
save = True
# Variable units: rho (kg/m^3), Vp (km/s), Vs (km/s)
radius, _, _, density, vp, vs = np.loadtxt("V1-Th.out", skiprows=1).T

if equal_spacing:
    # Find layer boundaries for each model based on jumps in values
    # Only do this for the first (density), then share with other values
    diffs = density[:-1] - density[1:]
    # Looking for indices for the 2 largest difference values
    bigval = np.sort(diffs)[-100]
    big_idxs = np.argwhere(diffs >= bigval)[:,0].tolist()
    print(radius[big_idxs]*1000)
    idxs = []
    for i in range(0,len(radius), 4):
        idxs.append(i)
    for idx in big_idxs:
        if idx not in idxs:
            idxs.append(idx)
        else:
            idxs.append(idx-1)
    idxs = sorted(idxs)
    idxs.append(len(radius)-1)   

else:
    # Find layer boundaries for each model based on jumps in values
    # Only do this for the first (density), then share with other values
    diffs = density[:-1] - density[1:]
    # Looking for indices for the 2 largest difference values
    bigval = np.sort(diffs)[-134]
    idxs = np.argwhere(diffs >= bigval)[:,0].tolist()
    idxs.append(len(radius)-1)
if save:
    output = open("model_layers.txt", "w")
    for i, idx in enumerate(idxs):
        rad = np.round(radius[idx]*1000, 0)
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
    for i, idx in enumerate(idxs):
        dens = np.round((density[idx]/1000), 4)
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
    for i, idx in enumerate(idxs):
        vel_p = np.round(vp[idx], 4)
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
    for i, idx in enumerate(idxs):
        vel_s = np.round(vs[idx], 4)
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

    output.close()
