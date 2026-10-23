
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
m1 =False
m2 =True
if m1:
    # plot a record section from a list of sem files (stacked, amplitude-normalized)
    fig, ax = plt.subplots(1, 3, figsize=(12, 5))
    fids = [
        'XX.S075.BXX.semd', 'XX.S060.BXX.semd',
        'XX.S045.BXX.semd', 'XX.S030.BXX.semd', 'XX.S015.BXX.semd',
        'XX.S000.BXX.semd', 'XX.SN15.BXX.semd', 'XX.SN30.BXX.semd',
        'XX.SN45.BXX.semd', 'XX.SN60.BXX.semd', 'XX.SN75.BXX.semd',
        'XX.SN90.BXX.semd'
    ]
    folders = ['V1-Tc','V1-Th','V4-Tc']

    for i,folder in enumerate(folders):
        trs = []
        labels = []
        for fid in fids:
            st = read_sem(folder+'/'+fid, origintime="1970-01-01T00:00:00", source=None, stations=None,
                        location="", precision=4, source_format="CMTSOLUTION")
            tr = st[0]
            cutoff = 0.018 
            tr.filter('lowpass', freq=cutoff, corners=4, zerophase=True)

            # append a copy to avoid accidental shared/mutated data between traces
            trs.append(tr.copy())
            labels.append(tr.stats.station if tr.stats.station else os.path.basename(fid))

        # determine normalization scale (so traces visually comparable)
        max_amp = max((np.nanmax(np.abs(tr.data)) for tr in trs))
        spacing = 1.0                      # vertical spacing between traces (in y units)
        amp_scale = 0.8 * spacing / max_amp  # scale so peaks occupy ~80% of spacing
        y_positions = np.arange(len(trs))[::-1]  # top-to-bottom stacking

        for idx, tr in enumerate(trs):
            y = y_positions[idx]
            t = tr.times()
            scaled = tr.data * amp_scale + y
            ax[i].plot(t, scaled, color='k', linewidth=0.7)
            if i == 0:  
                ax[i].text(-0.5, y, labels[idx],
                        verticalalignment='center', horizontalalignment='right',
                        fontsize=8)
        ax[i].set_title(folder)
        #Label y axis with amplification factor
        if i == 0:
            ax[i].set_ylabel(f"Normalized Amplitude of Displacement")

            ax[i].yaxis.set_label_coords(-0.1, 0.5)
        ax[i].yaxis.set_ticks([])
        ax[i].set_ylim(-1, len(trs))
        ax[i].set_yticks(y_positions)
        ax[i].set_yticklabels([])  
        ax[i].set_xlabel("Time (s)")
        ax[i].set_xlim(0, 7000)
    plt.show()
    #1e-6
if m2:
    # plot a record section from a list of sem files (stacked, amplitude-normalized)
    fig, ax = plt.subplots(3, 1, figsize=(4, 5))
    fids = [ 'XX.SN90.BXX.semd'
    ]
    folders = ['V1-Tc','V1-Th','V4-Tc']

    for i,folder in enumerate(folders):
        trs = []
        labels = []
        for fid in fids:
            st = read_sem(folder+'/'+fid, origintime="1970-01-01T00:00:00", source=None, stations=None,
                        location="", precision=4, source_format="CMTSOLUTION")
            tr = st[0]
            cutoff = 0.018 
            tr.filter('lowpass', freq=cutoff, corners=4, zerophase=True)

            # append a copy to avoid accidental shared/mutated data between traces
            trs.append(tr.copy())
            labels.append(tr.stats.station if tr.stats.station else os.path.basename(fid))


        for idx, tr in enumerate(trs):
            t = tr.times()
            ax[i].plot(t, tr.data, color='k', linewidth=0.7)

        ax[i].set_title(folder)
        ax[i].set_xlim(0, 7000)
        #Label y axis with amplification factor
        if i == 2:
            ax[i].set_xlabel("Time (s)")

        else:
            ax[i].set_xticklabels([])  
    plt.show()
    #1e-6