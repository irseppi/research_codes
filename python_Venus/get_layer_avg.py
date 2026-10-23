import numpy as np


fid = "V1-Tc.out"
depth, _, _, density, vp, vs = np.loadtxt(fid, skiprows=1).T
depth = depth[::-1]

depth_idxs = [0, len(depth) - 500, len(depth) - 495, len(depth) - 439, len(depth) - 276, -1]

            # 0  700 2950 6015
print(depth_idxs)
for i, top in enumerate(depth_idxs[:-1]):
    bottom = depth_idxs[i+1]
    print(f"[{depth[top]}-{depth[bottom]}]")
    print(f"rho = {density[top:bottom].mean():.2f}")
    print(f"Vp  = {vp[top:bottom].mean():.2f}")
    print(f"Vs] = {vs[top:bottom].mean():.2f}\n")

'''
fid = "V1-Th.out"
depth, _, _, density, vp, vs = np.loadtxt(fid, skiprows=1).T
depth = depth[::-1]

depth_idxs = [0, len(depth) - 292, len(depth) - 245, 503, -1]
            # 0  700 2950 6015

for i, top in enumerate(depth_idxs[:-1]):
    bottom = depth_idxs[i+1]
    print(f"[{depth[top]}-{depth[bottom]}]")
    print(f"rho = {density[top:bottom].mean():.2f}")
    print(f"Vp  = {vp[top:bottom].mean():.2f}")
    print(f"Vs] = {vs[top:bottom].mean():.2f}\n")
'''