# class that tracks global cryptocurrency market data acquired from a Json file from
# the source coincheckup.com
# created for use in CryptoData.py
# by Mitul Saha


class Tracker:
    aggr = ''
    type = ''
    avg = 0
    min = 0
    max = 0
    dps = 0

    def __init__(self, aggr, type):
        self.aggr = aggr
        self.type = type
        self.avg = 0
        self.min = 0
        self.max = 0
        self.dps = 0

    def csvadd(self):
        return "%s,%s,%d,%d,%d\n" % (self.aggr, self.type, self.avg,
                                     self.min, self.max)

    def compute(self, data, start=0):
        self.min = data[start]
        self.max = data[start]

        for point in data:
            self.dps += 1
            self.avg += point
            if point < self.min:
                self.min = point
            elif point > self.max:
                self.max = point

        self.avg = self.avg / self.dps

