# suite of functions to assist in logging generic programs
# includes time stamp converters for special use in CryptoData.py
# __author__ = 'jordi.terns'

import os
import sys
import logging
import time
import datetime

class LogHelper(object):

    def __init__(self, OutDirectory, LoggerId):
        try:
            if not os.path.exists(OutDirectory):
                os.makedirs(OutDirectory)

            DateAux = (datetime.date.today()).strftime("%Y-%m-%d")
            CurrentTime = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
            LogFile = OutDirectory + "/" + DateAux + "-" + LoggerId + ".log"

            self.logger = logging.getLogger(LoggerId)
            hdlr = logging.FileHandler(LogFile)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)
            self.logger.setLevel(logging.INFO)

            self.logger.info("---------------------------------------------------------------------------")
            self.logger.info("|" + '{:^73}'.format(CurrentTime) + "|")
            self.logger.info("---------------------------------------------------------------------------")
            self.logger.info("")

        except Exception as e:
            print("Error: LogHelper >> Constructor > " + str(e))
            sys.exit(99)


    def Error(self, msg, display=False):
        try:
            self.logger.error(msg)
            if display: print(self.__getTimeStamp() + " > " + msg)

        except Exception as e:
            print("LogHelper >> Error > " + str(e))


    def Info(self, msg, display=False):
        try:
            self.logger.info(msg)
            if display: print(self.__getTimeStamp() + " > " + msg)

        except Exception as e:
            print("LogHelper >> Info > " + str(e))

    def __getTimeStamp(self):
        try:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        except Exception as e:
            self.Error("LogHelper >> __getTimeStamp > " + str(e))


def _get_unix_timestamp(logger, date_string):
    try:
        unix_time = time.mktime(datetime.datetime.strptime(date_string, "%Y-%m-%d").timetuple())

        return int(unix_time) * 1000

    except Exception as e:
        logger.Error('CoinCheckupAPI >> _get_unix_timestamp > ' + str(e))


def _get_date(logger, unix_timestamp: int) -> str:
    try:
        correct_timestamp = int(unix_timestamp / 1000)

        return datetime.datetime.fromtimestamp(correct_timestamp).strftime('%Y-%m-%d')

    except Exception as e:
        logger.Error('CoinCheckupAPI >> _get_date > ' + str(e))
