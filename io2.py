
import os
import numpy as np
from matplotlib import pyplot as plt
from obspy import UTCDateTime, Stream, Trace

from pysep import logger
from pysep.utils.cap_sac import append_sac_headers, append_sac_headers_cartesian


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



from obspy.imaging.beachball import beachball

'''
 MLI 1977  7  8  6 23  2.40  10.9400   39.6300  38.0 5.0 0.0 ETHIOPIA                                
event name:     070877B        
time shift:      5.8000
half duration:   1.8000
latitude:       10.4200
longitude:      39.9800
depth:          15.0000
Mrr:      -3.590000e+23
Mtt:      -9.170000e+23
Mpp:       1.277000e+24
Mrt:       2.390000e+23
Mrp:       3.370000e+23
Mtp:      -2.240000e+23
'''
#mt = [-3.59, -9.17, 0, 2.39, 0, 0]
#beachball(mt, size=200, linewidth=2, facecolor='b')

# ['XX.S090.BXX.semd', 'XX.S090.BXZ.semd', 'XX.S075.BXX.semd', 'XX.S075.BXZ.semd', 'XX.S060.BXX.semd',
#  'XX.S060.BXZ.semd', 'XX.S045.BXX.semd', 'XX.S045.BXZ.semd', 'XX.S030.BXX.semd', 'XX.S030.BXZ.semd',
#  'XX.S015.BXX.semd', 'XX.S015.BXZ.semd', 'XX.S000.BXX.semd', 'XX.S000.BXZ.semd',
#  'XX.SN15.BXX.semd', 'XX.SN15.BXZ.semd', 'XX.SN30.BXX.semd', 'XX.SN30.BXZ.semd',
#  'XX.SN45.BXX.semd', 'XX.SN45.BXZ.semd', 'XX.SN60.BXX.semd', 'XX.SN60.BXZ.semd',
#  'XX.SN75.BXX.semd', 'XX.SN75.BXZ.semd', 'XX.SN90.BXX.semd', 'XX.SN90.BXZ.semd']

# fig, ax = plt.subplots(13,1,figsize=(4,4), sharex=True)
# for i, fid in enumerate([
#     'XX.S090.BXX.semd', 'XX.S075.BXX.semd', 'XX.S060.BXX.semd',
#     'XX.S045.BXX.semd', 'XX.S030.BXX.semd', 'XX.S015.BXX.semd',
#     'XX.S000.BXX.semd', 'XX.SN15.BXX.semd', 'XX.SN30.BXX.semd',
#     'XX.SN45.BXX.semd', 'XX.SN60.BXX.semd', 'XX.SN75.BXX.semd',
#     'XX.SN90.BXX.semd']):
#     st = read_sem(fid, origintime="1970-01-01T00:00:00", source=None, stations=None,
#                   location="", precision=4, source_format="CMTSOLUTION")
#     tr = st[0]
#     distance = i * 15 * 111194.9
#     ax[i].plot(tr.times(), tr.data, color='red')
#     #plt.plot(tr.times("matplotlib"), tr.data + distance, color='red')
# plt.xlim(0, 2000)
# plt.show()

#'XX.S090.BXX.semd',
# plot a record section from a list of sem files (stacked, amplitude-normalized)
fids = [
    'XX.S075.BXX.semd', 'XX.S060.BXX.semd',
    'XX.S045.BXX.semd', 'XX.S030.BXX.semd', 'XX.S015.BXX.semd',
    'XX.S000.BXX.semd', 'XX.SN15.BXX.semd', 'XX.SN30.BXX.semd',
    'XX.SN45.BXX.semd', 'XX.SN60.BXX.semd', 'XX.SN75.BXX.semd',
    'XX.SN90.BXX.semd'
]
folders = ['V1-Tc','V1-Th','V4-Tc',"V4-Th","V5-Tc","V5-Th"]

for i,folder in enumerate(folders):

    trs = []
    labels = []
    for fid in fids:
        st = read_sem(folder+'/waveforms/'+fid, origintime="1970-01-01T00:00:00", source=None, stations=None,
                    location="", precision=4, source_format="CMTSOLUTION")
        tr = st[0]
        # low-pass filter: remove any frequency above 0.025 Hz
        cutoff = 0.018 #0.025
        nyquist = 0.5 / tr.stats.delta
        if cutoff < nyquist:
            tr.filter('lowpass', freq=cutoff, corners=4, zerophase=True)
        else:
            logger.warning(f"cutoff {cutoff} Hz >= Nyquist {nyquist:.3f} Hz; skipping filter")
        # append a copy to avoid accidental shared/mutated data between traces
        trs.append(tr.copy())
        labels.append(tr.stats.station if tr.stats.station else os.path.basename(fid))

    # determine normalization scale (so traces visually comparable)
    # use nan-safe max and handle empty or zero amplitude cases
    max_amp = max((np.nanmax(np.abs(tr.data)) for tr in trs))

    #max_amp = 739371188223.9657 * 50
    spacing = 1.0                      # vertical spacing between traces (in y units)
    amp_scale = 0.8 * spacing / max_amp  # scale so peaks occupy ~80% of spacing

    fig, ax = plt.subplots(1, 1, figsize=(4, 5))
    y_positions = np.arange(len(trs))[::-1]  # top-to-bottom stacking

    for idx, tr in enumerate(trs):
        #max_amp = np.nanmax(np.abs(tr.data)) 
        #spacing = 1.0                      # vertical spacing between traces (in y units)
        #amp_scale = 0.8 * spacing / max_amp  # scale so peaks occupy ~80% of spacing
        y = y_positions[idx]
        t = tr.times()
        scaled = tr.data * amp_scale + y
        ax.plot(t, scaled, color='k', linewidth=0.7)
        # station label on the left
        # place station label just outside the left of the axes, vertically centered on trace
        ax.text(-0.5, y, labels[idx],
                verticalalignment='center', horizontalalignment='right',
                fontsize=8)
    #Label y axis with amplification factor
    ax.set_ylabel(f"Amplitude (x{amp_scale:.1e})")
    # move y label to left more
    ax.yaxis.set_label_coords(-0.1, 0.5)
    #remove tick marks of x axis
    ax.yaxis.set_ticks([])
    ax.set_ylim(-1, len(trs))
    ax.set_title(folder)
    ax.set_yticks(y_positions)
    ax.set_yticklabels([])  # labels drawn with text; hide default ticks
    ax.set_xlabel("Time (s)")
    #ax.set_xlim(0, 2500)
    plt.savefig(f"{folder}_record_section.png", dpi=300, bbox_inches='tight')
