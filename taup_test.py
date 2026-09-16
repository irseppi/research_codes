

import os
import numpy as np

from pysep import logger
from collections import defaultdict
from matplotlib import pyplot as plt
from obspy import UTCDateTime, Stream, Trace
from obspy.taup import TauPyModel, taup_create
from pysep.utils.cap_sac import append_sac_headers, append_sac_headers_cartesian
from obspy.taup import plot_travel_times
def read_sem(fid, origintime="1970-01-01T00:00:00", source=None, stations=None, 
             location="", precision=4, source_format="CMTSOLUTION"):
    """
    Specfem3D outputs seismograms to ASCII (.sem? or .sem.ascii) files.
    Converts SPECFEM synthetics into ObsPy Stream objects with the correct
    header information. If `source` and `stations` files are also provided,
    PySEP will write appropriate SAC headers to the underlying data.

    :type fid: str
    :param fid: path of the given ascii file
    :type origintime: obspy.UTCDateTime
    :param origintime: UTCDatetime object for the origintime of the event. If
        None given, defaults to dummy value of '1970-01-01T00:00:00'
    :type source: str
    :param source: optional SPECFEM source file (e.g., CMTSOLUTION, SOURCE)
        defining the event which generated the synthetics. Used to grab event
        information and append as SAC headers to the ObsPy Stream
    :type stations: str
    :param stations: optional STATIONS file defining the station locations for
        the SPECFEM generated synthetics, used to generate SAC headers
    :type location: str
    :param location: location value for a given station/component
    :type precision: int
    :param precision: dt precision determined by differencing two
        adjancent time steps in the underlying ascii text file.
    :rtype st: obspy.Stream.stream
    :return st: stream containing header and data info taken from ascii file
    """
    # This was tested up to SPECFEM3D Cartesian git version 6895e2f7
    try:
        times = np.loadtxt(fname=fid, usecols=0)
        data = np.loadtxt(fname=fid, usecols=1)

    # At some point in 2018, the Specfem developers changed how the ascii files
    # were formatted from two columns to comma separated values, and repeat
    # values represented as 2*value_float where value_float represents the data
    # value as a float
    except ValueError:
        times, data = [], []
        with open(fid, 'r') as f:
            lines = f.readlines()
        for line in lines:
            try:
                time_, data_ = line.strip().split(',')
            except ValueError:
                if "*" in line:
                    time_ = data_ = line.split('*')[-1]
                else:
                    raise ValueError
            times.append(float(time_))
            data.append(float(data_))

        times = np.array(times)
        data = np.array(data)

    # We assume that dt is constant after 'precision' decimal points
    delta = round(times[1] - times[0], precision)

    # Get metadata information from CMTSOLUTION and STATIONS files
    event = None
    if source is None:
        origintime = UTCDateTime(origintime)
    else:
        event = read_events_plus(source, format=source_format)[0]
        origintime = event.preferred_origin().time
        logger.info(f"reading origintime from event: {origintime}")

    # Honor that Specfem doesn't start exactly on 0 due to USER_T0
    origintime += times[0]

    # SPECFEM2D/SPECFEM3D_Cartesian style name format, e.g., NZ.BFZ.BXE.semd OR
    # SPECFEM3D_Globe style name format, e.g., TA.O20K.BXR.sem.ascii
    net, sta, cha, fmt, *_ = os.path.basename(fid).split(".")
    stats = {"network": net, "station": sta, "location": location,
             "channel": cha, "starttime": origintime, "npts": len(data),
             "delta": delta, "mseed": {"dataquality": 'D'}, "format": fmt
             }
    st = Stream([Trace(data=data, header=stats)])

    if event and stations:
        try:
            # `read_stations` will throw a ValueError for Cartesian coordinates
            inv = read_stations(stations)
            st = append_sac_headers(st, event, inv)
        except ValueError as e:
            # If Cartesian coordinate system, slightly different header approach
            st = append_sac_headers_cartesian(st, event, stations)
        # Broad catch here as this is an optional step that might not always
        # work or be possible
        except Exception as e:
            logger.warning(f"could not append SAC header to trace because {e}")

    return st


fids = [
    'XX.S075.BXX.semd', 'XX.S060.BXX.semd',
    'XX.S045.BXX.semd', 'XX.S030.BXX.semd', 'XX.S015.BXX.semd',
    'XX.S000.BXX.semd', 'XX.SN15.BXX.semd', 'XX.SN30.BXX.semd',
    'XX.SN45.BXX.semd', 'XX.SN60.BXX.semd', 'XX.SN75.BXX.semd',
    'XX.SN90.BXX.semd'
]

folders = ['V1-Tc']
event_depth = 0 #km
cutoff = 0.027980241614718911 #from specfem

trs = {}

taup_create.build_taup_model("V1-Tc.tvel")
model = TauPyModel(model="V1-Tc")
fig, ax = plt.subplots(figsize=(9, 9))
ax = plot_travel_times(source_depth=0, phase_list=["ttbasic"], model=model,
                    ax=ax, fig=fig)

dist_degree = 0
dist_degree_hold = 15  
phase_dict = defaultdict(list)
for jj, fid in enumerate(fids):
    st = read_sem('V1-Tc_folder/waveforms/'+fid, origintime="1970-01-01T00:00:00",
                    source=None, stations=None, location="", precision=4, 
                    source_format="CMTSOLUTION")
    
    tr = st[0]
    dist_degree = dist_degree_hold
    dist_degree_hold += 15
    #arrivals = model.get_ray_paths(source_depth_in_km=0, 
    #                               distance_in_degree=dist_degree, 
    #                               phase_list=['P', 'S', 'PP', 'SS'])
    #ax = arrivals.plot_rays(plot_type="cartesian")

    tr.filter('lowpass', freq=cutoff, corners=4, zerophase=True)

    trs[dist_degree] = tr.copy()


    arrival_s = model.get_travel_times(source_depth_in_km=event_depth,
                                        distance_in_degree=dist_degree,
                                        phase_list=['P', 'S', 'PP', 'SS'])
    # Keep only the earliest (first) arrival for each phase at this distance.
    first_arrivals = {}
    for a in arrival_s:
        if a.name not in first_arrivals or a.time < first_arrivals[a.name].time:
            first_arrivals[a.name] = a

    for a in first_arrivals.values():
        print(fid, a.name, a.time)
        phase_dict[a.name].append((dist_degree, a.time))
        

# determine normalization scale (so traces visually comparable)
max_amp = max((np.nanmax(np.abs(trs[dist_degree].data)) for dist_degree in trs.keys()))
spacing = list(trs.keys())[1] - list(trs.keys())[0] # vertical spacing between traces (in y units)
amp_scale = 0.8 * spacing / max_amp  # scale so peaks occupy ~80% of spacing

colors = {phase: plt.cm.tab20(i % 20) for i, phase in enumerate(phase_dict.keys())}

fig, ax = plt.subplots(1, 1, figsize=(4, 5))

for d, tr in trs.items():
    t = tr.times()
    scaled = tr.data * amp_scale + d
    ax.plot(t, scaled, color='k', linewidth=0.7)

arrival_half_height = 0.4 * 0.8 * spacing
for phase in phase_dict.keys():
    pts = phase_dict[phase]
    ys, xs = [d for d, t in pts], [t for d, t in pts]

    ax.vlines(xs, ymin=[y - arrival_half_height for y in ys],
              ymax=[y + arrival_half_height for y in ys],
              colors=colors[phase], linewidth=1.0, alpha=0.9,
              label=phase, zorder=100)

ax.set_ylabel(f"Amplitude (x{amp_scale:.1e})")
ax.set_xlabel("Time (s)")
ax.legend(loc='upper right', fontsize=8, frameon=True, framealpha=0.9)
plt.show()
