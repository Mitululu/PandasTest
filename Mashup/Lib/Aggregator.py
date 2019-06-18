# aggregates the data from the json file from coincheckup.com
# either by month, quarter, or year

import datetime
import pandas as pd

from Lib import CryptoTrack


def aggregate(data, type, aggr, stime, etime):
    pddata = {"timestamp": [], "usd": [], aggr: [], "type": []}

    for dpoint in data:
        if dpoint[0] > stime and dpoint[0] < etime:
            pddata["timestamp"].append(dpoint[0])
            pddata["usd"].append(dpoint[1])
            pddata["type"].append(type)

            if aggr == "month":
                pddata[aggr].append(getmonth(dpoint[0]))
            elif aggr == "quarter":
                pddata[aggr].append(getquarter(dpoint[0]))
            else:
                # default to year if neither month nor quarter
                pddata[aggr].append(getyear(dpoint[0]))

        if dpoint[0] > etime:
            break

    pddata = pd.DataFrame(pddata)
    current = 0
    curragg = pddata[aggr][current]
    output = []

    while True:
        pdcurr = pddata[pddata[aggr] == curragg]
        track = CryptoTrack.Tracker(curragg, type)
        track.compute(pdcurr["usd"], start=current)
        output.append(track)

        try:
            while curragg == pddata[aggr][current]:
                current += 1
            curragg = pddata[aggr][current]
        except LookupError:
            break

    return output



def getmonth(timestamp):
    correct_timestamp = int(timestamp / 1000)
    return datetime.datetime.fromtimestamp(correct_timestamp).strftime('%Y-%m')


def getquarter(timestamp):
    correct_timestamp = int(timestamp / 1000)
    month = int(datetime.datetime.fromtimestamp(correct_timestamp).strftime('%m'))
    year = datetime.datetime.fromtimestamp(correct_timestamp).strftime('%Y-')

    if month < 4:
        return year + 'Q1'
    elif month < 7:
        return year + 'Q2'
    elif month < 10:
        return year + 'Q3'
    return year + 'Q4'


def getyear(timestamp):
    correct_timestamp = int(timestamp / 1000)
    return datetime.datetime.fromtimestamp(correct_timestamp).strftime('%Y')
