# class that tracks global cryptocurrency market data acquired from a Json file from
# the source coincheckup.com
# created for use in CryptoData.py
# by Mitul Saha


class Tracker:
    avg = 0
    min = 0
    max = 0
    dps = 0

    def __init__(self):
        self.avg = 0
        self.min = 0
        self.max = 0
        self.dps = 0

    def compute(self, data):
        self.min = data[0][1]
        self.max = data[0][1]

        for point in data:
            self.dps += 1
            self.avg += point[1]
            if point[1] < self.min:
                self.min = point[1]
            elif point[1] > self.max:
                self.max = point[1]

        self.avg = self.avg / self.dps