# aggregates the data from the json file from coincheckup.com
# either by month, quarter, or year

import datetime
import pandas as pd

from Lib import LogHelper
from Lib import CryptoTrack

def getGroup()

def aggrYear(logger, data, iscap, year):
    ind = -1
    newData = []

    while True:
        ind += 1
        curyear = int((logger._get_date(data[ind][0])).year)
        if curyear == year:
            break

    while curyear == year:
        newData.append(data[ind])
        ind += 1
        curyear = int((logger._get_date(data[ind][0])).year)

    track = CryptoTrack.Tracker()
    track.compute(newData)

    output = [str(year)]
    if iscap:
        output.append("market cap")
    else
        output.append("volume")
    output.append(track.avg)
    output.append(track.max)
    output.append(track.min)

    return output


def aggrQuarter(logger, data, iscap, year, quarter):
    ind = -1
    newData = []

    while True:
        ind += 1
        curyear = int((logger._get_date(data[ind][0])).year)
        if curyear == year:
            break

    while curyear == year:
        newData.append(data[ind])
        ind += 1
        curyear = int((logger._get_date(data[ind][0])).year)

    track = CryptoTrack.Tracker()
    track.compute(newData)

    output = [str(year)]
    if iscap:
        output.append("market cap")
    else
        output.append("volume")
    output.append(track.avg)
    output.append(track.max)
    output.append(track.min)

    return output


def aggrMonth(logger, data, iscap, year, month):
    ind = -1
    newData = []

    while True:
        ind += 1
        curyear = int((logger._get_date(data[ind][0])).year)
        if curyear == year:
            break

    while curyear == year:
        newData.append(data[ind])
        ind += 1
        curyear = int((logger._get_date(data[ind][0])).year)

    track = CryptoTrack.Tracker()
    track.compute(newData)

    output = [str(year)]
    if iscap:
        output.append("market cap")
    else
        output.append("volume")
    output.append(track.avg)
    output.append(track.max)
    output.append(track.min)

    return output
