import numpy as np

from collections import defaultdict
from matplotlib import pyplot as plt
from obspy.taup import TauPyModel, taup_create
'''
model_names = ["iasp91", "V1-Tc"]
taup_create.build_taup_model("V1-Tc.tvel")
models = [TauPyModel(model=name) for name in model_names]
distances = np.linspace(0.1, 180.0, 1800)

phase_sets = []
for model in models:
    phase_set = set()
    for distance in distances:
        phase_set.update(
            arrival.name
            for arrival in model.get_travel_times(
                source_depth_in_km=0.0,
                distance_in_degree=float(distance),
                phase_list=["ttall"],
            )
        )
    phase_sets.append(phase_set)

phases = sorted(set.union(*phase_sets))
phase_colors = dict(zip(phases, plt.cm.tab20(np.linspace(0, 1, len(phases)))))
fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

for ax, model_name, model, available_phases in zip(
        axes, model_names, models, phase_sets):
    curves = defaultdict(list)
    for distance in distances:
        for arrival in model.get_travel_times(
                source_depth_in_km=0.0,
                distance_in_degree=float(distance),
                phase_list=["ttall"]):
            curves[arrival.name].append((distance, arrival.time))
    for phase in sorted(available_phases):
        points = np.asarray(curves[phase])
        ax.scatter(points[:, 0], points[:, 1], color=phase_colors[phase],
                linewidth=0.01, label=phase)
    ax.set_title(model_name)
    ax.set_xlabel("Distance (degrees)")
    ax.grid(True, alpha=0.25)
    ax.set_xlim(0, 180)
axes[0].set_ylabel("Travel time (seconds)")

handles = [plt.Line2D([], [], color=phase_colors[phase], label=phase)
           for phase in phases]
fig.legend(handles=handles, loc="center left", bbox_to_anchor=(0.76, 0.5),
           ncol=2, frameon=True)
fig.tight_layout(rect=(0, 0, 0.74, 1))
plt.show()
'''

model_names = ["V1-Tc", "iasp91"]
taup_create.build_taup_model("V1-Tc.tvel")
models = [TauPyModel(model=name) for name in model_names]
distances = np.linspace(0.1, 180.0, 1800)

fig, ax = plt.subplots(figsize=(12, 6))

for model_name, model, color in zip(model_names, models, ["black", "red"]):
    curves = defaultdict(list)
    for distance in distances:
        arrivals = model.get_travel_times(
            source_depth_in_km=0.0,
            distance_in_degree=float(distance),
            phase_list=["ttall"],
        )
        for arrival in arrivals:
            curves[arrival.name].append((float(distance), arrival.time))

    for phase in sorted(curves):
        xs, ys = np.asarray(curves[phase], dtype=float).T
        ax.scatter(xs, ys, color=color, linewidth=0.0001, alpha=0.8, label=model_name)

ax.set_title("Venus (black) vs Earth (red) Travel Times")
ax.set_xlabel("Distance (degrees)")
ax.set_ylabel("Travel time (seconds)")
ax.grid(True, alpha=0.25)
ax.set_xlim(0, 180)
fig.tight_layout()
plt.show()

