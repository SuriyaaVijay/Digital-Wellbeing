
""" legacy_split_events.py for uLogMe:

Usage:
$ legacy_split_events.py

Old file, to convert old log files in text (.txt) format in the uLogMe/logs/ folder, and generate the JSON files in uLogMe/render/json/ folder.

Note: works in both Python 2 and 3.
"""
from __future__ import print_function   # Python 2 compatibility
from __future__ import absolute_import  # Python 2 compatibility

import datetime
import os
import os.path

mint = -1
maxt = -1

ROOT = ""
RENDER_ROOT = os.path.join(ROOT, "render")


def loadEvents(fname):
    """
    Reads a file that consists of first column of unix timestamps
    followed by arbitrary string, one per line. Outputs as dictionary.
    Also keeps track of min and max time seen in global mint,maxt
    """
    global mint, maxt  # not proud of this, okay?
    events = []

    try:
        with open(fname, "r") as thisfile:
            ws = thisfile.read().splitlines()
        events = []
        for w in ws:
            ix = w.find(" ")  # find first space, that's where stamp ends
            stamp = int(w[:ix])
            sstr = w[ix + 1:]
            events.append({"t": stamp, "s": sstr})
            if stamp < mint or mint == -1:
                mint = stamp
            if stamp > maxt or maxt == -1:
                maxt = stamp
    except Exception as e:
        print("could not load %s. Setting empty events list." % (fname, ))
        print("(this is probably OKAY by the way, just letting you know)")
        print(e)
        events = []
    return events


if __name__ == "__main__":
    # load all window events
    active_window_file = os.path.join(ROOT, "..", "logs", "activewin.txt")
    print("loading windows events...")
    wevents = loadEvents(active_window_file)

    # load all keypress events
    keyfreq_file = os.path.join(ROOT, "..", "logs", "keyfreq.txt")
    print("loading key frequencies...")
    kevents = loadEvents(keyfreq_file)
    for k in kevents:  # convert the key frequency to just be an int, not string
        k["s"] = int(k["s"])

    print("loading notes...")
    notes_file = os.path.join(ROOT, "..", "logs", "notes.txt")
    nevents = loadEvents(notes_file)

    # rewind time to 7am on earliest data collection day
    dfirst = datetime.datetime.fromtimestamp(mint)
    dfirst = datetime.datetime(dfirst.year, dfirst.month, dfirst.day, 7)  # set hour to 7am
    curtime = int(dfirst.strftime("%s"))
    out_list = []

    while curtime < maxt:
        t0 = curtime
        t1 = curtime + 60 * 60 * 24  # one day later
        # this will break if there are leap seconds... sigh :D

        # filter events
        e1 = [x for x in wevents if x["t"] >= t0 and x["t"] < t1]
        e2 = [x for x in kevents if x["t"] >= t0 and x["t"] < t1]
        e3 = [x for x in nevents if x["t"] >= t0 and x["t"] < t1]

        # sort by time just in case
        e1.sort(key=lambda x: x["t"])
        e2.sort(key=lambda x: x["t"])
        e3.sort(key=lambda x: x["t"])

        # write out log files split up
        if e3:
            fout = os.path.join(ROOT, "..", "logs", "notes_%d.txt" % (t0, ))
            with open(fout, "w") as thisotherfile:
                thisotherfile.write("".join(["%d %s\n" % (x["t"], x["s"]) for x in e3]))
            print("wrote to", fout)

        if e2:
            fout = os.path.join(ROOT, "..", "logs", "keyfreq_%d.txt" % (t0, ))
            with open(fout, "w") as thisotherfile:
                thisotherfile.write("".join(["%d %s\n" % (x["t"], x["s"]) for x in e2]))
            print("wrote to", fout)

        if e1:
            fout = os.path.join(ROOT, "..", "logs", "window_%d.txt" % (t0, ))
            with open(fout, "w") as thisotherfile:
                thisotherfile.write("".join(["%d %s\n" % (x["t"], x["s"]) for x in e1]))
            print("wrote to", fout)

        curtime += 60 * 60 * 24
