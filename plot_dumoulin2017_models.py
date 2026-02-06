"""
Plot 1D velocity profiles from Dumoulin et al. 2017, files were sent to me
by Indujaa G. after she requested them from Caroline.
"""
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

def set_plot_aesthetic(
        ax, ytick_fontsize=5., xtick_fontsize=5., tick_linewidth=1.5,
        tick_length=5., tick_direction="in", xlabel_fontsize=8.,
        ylabel_fontsize=8., axis_linewidth=1.5, spine_zorder=8, 
        title_fontsize=9., axis_color="k", xtick_fontcolor="k", 
        ytick_fontcolor="k", ylabel_fontcolor="k", xlabel_fontcolor="k",
        spine_top=True, spine_bot=True, spine_left=True, spine_right=True, 
        xtick_minor=None, xtick_major=None, ytick_minor=None, ytick_major=None,
        xgrid_major=True, xgrid_minor=True, ygrid_major=True, ygrid_minor=True,
        **kwargs):
    """
    Set a uniform look for figures, stolen from PySEP
    """
    ax.title.set_fontsize(title_fontsize)
    ax.tick_params(axis="both", which="both", width=tick_linewidth,
                        direction=tick_direction, length=tick_length)
    ax.tick_params(axis="x", labelsize=xtick_fontsize, colors=xtick_fontcolor)
    ax.tick_params(axis="y", labelsize=ytick_fontsize, colors=ytick_fontcolor)
    ax.xaxis.label.set_size(xlabel_fontsize)
    ax.yaxis.label.set_size(ylabel_fontsize)

    # Thicken up the bounding axis lines
    for axis, flag in zip(["top", "bottom", "left", "right"],
                          [spine_top, spine_bot, spine_left, spine_right]):
        # Deal with the case where command line users are inputting strings
        if isinstance(flag, str):
            flag = bool(flag.capitalize() == "True")
        ax.spines[axis].set_visible(flag)
        ax.spines[axis].set_linewidth(axis_linewidth)

    # Set spines above azimuth bins
    for spine in ax.spines.values():
        spine.set_zorder(spine_zorder)
        spine.set_color(axis_color)

    # Set xtick label major and minor which is assumed to be a time series
    if xtick_major:
        ax.xaxis.set_major_locator(MultipleLocator(float(xtick_major)))
    if xtick_minor:
        ax.xaxis.set_minor_locator(MultipleLocator(float(xtick_minor)))
    if ytick_minor:
        ax.yaxis.set_major_locator(MultipleLocator(float(ytick_major)))
    if ytick_major:
        ax.yaxis.set_minor_locator(MultipleLocator(float(ytick_minor)))

    # Set color of axis and labels
    ax.xaxis.label.set_color(xlabel_fontcolor)
    ax.yaxis.label.set_color(ylabel_fontcolor)

    plt.sca(ax)
    if xgrid_major:
        plt.grid(visible=True, which="major", axis="x", alpha=0.2, linewidth=1)
    if xgrid_minor:
        plt.grid(visible=True, which="minor", axis="x", alpha=0.2, linewidth=.5)
    if ygrid_major:
        plt.grid(visible=True, which="major", axis="y", alpha=0.2, linewidth=1)
    if ygrid_minor:
        plt.grid(visible=True, which="minor", axis="y", alpha=0.2, linewidth=.5)

    plt.tight_layout()



# Start plotting here
choices = [2,3,4]
title = ["Temperature", "?", "Density", "P-wave Velocity", "S-wave Velocity"]
ylabel = ["Temp (K)", "?", "rho (kg/m^3)", "Vp (km/s)", "Vs (km/s)"]

# Read in the files used
values = {}
fids = sorted(glob("V[145]-*.out"))
colors = ["C3", "C0", "C1", "C2", "C4", "C5", "C6"] 
for fid in fids:
    depth, *variables = np.loadtxt(fid, skiprows=1).T
    values[fid.split(".")[0]] = variables

# Flip the depth axis so that 0 is the surface (not the core)
depth = depth[::-1]  

# Plot one paramter for all models on a single figure
idxs = {}
first = True
f, ax = plt.subplots(1,3,figsize=(9,4), dpi=200)
for i in range(len(variables)):
    if choices and i not in choices:
        continue

    for j, (name, value) in enumerate(values.items()):
        model = np.array(value[i])
        ax[i-2].plot(model, depth, colors[j], lw=1, label=name)
        
        # Find layer boundaries for each model based on jumps in values
        # Only do this for the first (density), then share with other values
        if first:
            diffs = model[:-1] - model[1:]
            # Looking for indices for the 3 largest difference values
            bigval = np.sort(diffs)[-3]
            idxs[name] = np.argwhere(diffs >= bigval)
        
            #for idx, layer in zip(idxs[name], ["CMB", "MTZ"]):
            for idx in zip(idxs[name]):
                #plt.annotate(layer, xy=(90, depth[idx]-20), c=colors[j], fontsize=8)
                #ax[i-2].axhline(depth[idx], c="k", linestyle="--", lw=1, zorder=10)
                #Print the index that of the layer boundary
                print(f"{name} boundary at depth {depth[idx][0]:.2f} km (idx {idx[0]})")

        # Between each layer, find the depth average for the given layer
        # Sorry this is pretty nasty, quick and dirty
        layers = [0] + [_[0] for _ in idxs[name]] + [-1]  
        for _k, k in enumerate(layers[:-1]):
            k = k
            l = layers[_k+1]
            average = model[k:l].mean()
            print(f"{name} ({title[i]}) {depth[k]:.2f}-{depth[l]:.2f} = {average:.2f}")

    ax[i-2].invert_yaxis()
    ax[i-2].set_ylim([depth.max(), 0])
    ax[i-2].set_ylabel("Depth (km)")
    ax[i-2].set_xlabel(ylabel[i])
    ax[i-2].set_title(title[i])

    # First (left-most) plot gets all the accoutrement
    if first:
        set_plot_aesthetic(ax[i-2])
        first = False
    else:
        set_plot_aesthetic(ax[i-2], ytick_fontcolor="w", ytick_fontsize=0, 
                           ylabel_fontcolor="w")

    xmin, xmax = ax[i-2].get_xlim()
plt.legend(fontsize=3)
plt.show()
plt.close("all")
