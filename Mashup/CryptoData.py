# creates a csv file that describes the market capitalization and traded volume of
# the global cryptocurrency market
# arguments are start and end dates, aggregation form (year, quarter, or month), and
# and optional filepath if the data is to be written to a csv file.
# all data is extracted from coincheckup.com
__author__ = 'mitul.saha'

import os
import sys
import argparse
import requests
import json

from Lib import LogHelper, Aggregator
from Lib.LogHelper import _get_unix_timestamp


def main():
    print("Parsing arguments...")

    parser = argparse.ArgumentParser(description='Parse market data input')
    parser.add_argument('-s', '--startDate', action='store', dest="startDate",
                        help="string start date in form yyyy-mm-dd")
    parser.add_argument('-e', '--endDate', action='store', dest="endDate",
                        help="string end date in form yyyy-mm-dd")
    parser.add_argument('-w', '--write', action='store_true',
                        help="if set, write to the filepath instead of console")
    parser.add_argument('-f', "--filepath", action="store", dest="filepath",
                        help='string filepath to which data may be written')
    parser.add_argument('-a', '--aggregation', action='store', dest='aggr',
                        help='either year, quarter, or month for each data point;'
                             'if not chosen, defaults to year')
    args = parser.parse_args()

    if args.startDate is None or args.endDate is None:
        print("Needs both start and end date arguments; check parameters")
        sys.exit(99)

    path = os.path.dirname(os.path.realpath(__file__))
    logDir = path + "/UsageLog"
    logger = LogHelper.LogHelper(logDir, "Mashup")

    try:
        start = _get_unix_timestamp(logger, args.startDate)
        end = _get_unix_timestamp(logger, args.endDate)
        if start is None or end is None:
            logger.Error("either start or end is not a proper date; recheck parameters")
            sys.exit(99)
    except Exception as e:
        logger.Error("start and end date were not formatted properly: " + str(e))
        sys.exit(99)

    if start >= end:
        logger.Error("The end date must come after the start date")
        sys.exit(99)

    if args.write:
        if not args.filepath.endswith(".csv"):
            logger.Error("file being written to must be of type csv")
            sys.exit(99)
        try:
            f = open(args.filepath, "w+")
            f.close()
        except Exception as e:
            logger.Error("%s is an invalid filepath; recheck parameters" % args.filepath)
            logger.Error("Error message: " + str(e))
            sys.exit(99)

    url = 'https://coincheckup.com/v2/graphs-prx/_mktcap/'\
          + str(start) + '/' + str(end) + '/'
    try:
        webfile = requests.get(url)
    except Exception as e:
        logger.Error("start and end dates did not yield proper results from "
                     "coincheckup.com; error message follows\n" + e)
        sys.exit(99)

    print("Argument checks passed...")

    if args.aggr != "month" and args.aggr != "quarter":
        args.aggr = "year"
    cap = (json.loads((webfile.content).decode('utf-8')))["market_cap_by_available_supply"]
    vol = (json.loads((webfile.content).decode('utf-8')))["volume_usd"]
    outputcsv = "Period,Market Type,Min Trade,Max Trade,Avg Trade\n"

    captrack = Aggregator.aggregate(cap, "market_cap", args.aggr, start, end)
    voltrack = Aggregator.aggregate(vol, "volume_usd", args.aggr, start, end)
    track = []

    for i in range(len(captrack)):
        track.append(captrack[i])
        track.append(voltrack[i])

    for x in track:
        outputcsv += x.csvadd()

    if not args.write:
        print(outputcsv)
    else:
        with open(args.filepath, 'w') as f:
            f.write(outputcsv)
            print("Finished writing to " + args.filepath)

    logger.Info("Crypto-market data written successfully")
    print("Process complete; check the usage log for details")


if __name__ == "__main__":
    main()
