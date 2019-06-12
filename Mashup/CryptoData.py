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

from Lib import LogHelper


def main():
    print("Parsing arguments...")

    parser = argparse.ArgumentParser(description='Parse market data input')
    parser.add_argument('-s', '--startDate', action='store', dest="startDate",
                        help="string start date in form %Y-%m-%d")
    parser.add_argument('-e', '--endDate', action='store', dest="endDate",
                        help="string end date in form %Y-%m-%d")
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
        start = logger._get_unix_timestamp(args.startDate)
        end = logger._get_unix_timestamp(args.endDate)
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
            if not os.path.exists(args.filepath):
                os.makedirs(args.filepath)
            f = open(args.filepath, "r")
            f.close()
        except Exception as e:
            logger.Error("%s is an invalid filepath; recheck parameters" % args.filepath)
            logger.Error("Error message: " + str(e))
            sys.exit(99)

    print("Arg checks passed...")

    url = 'https://coincheckup.com/v2/graphs-prx/_mktcap/'\
          + str(start) + '/' + str(end) + '/'
    jsonFile = requests.get(url)

    for dic in jsonFile:


if __name__ == "__main__":
    main()
