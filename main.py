#!/usr/bin/python3

from datetime import date, datetime
from math import floor


class SSTime(object):
    def __init__(self, year, month, date, ss):
        self.year = year
        self.month = month
        self.date = date
        self.ss = ss

    def __str__(self):
        ss = format(self.ss, ',.2f').replace(',', "'")
        return f"{self.year}-{self.month}-{self.date} {ss}"

    @classmethod
    def make(cls, time: datetime):
        # original idea: https://github.com/cosmolabs-ru/sssync/blob/master/main.py
        dt = time.timetuple()
        hour = dt.tm_hour - 2
        if hour < 0:
            hour = 24 + hour
        ss = (hour * 3600 + dt.tm_min * 60 + dt.tm_sec) * (1000/864)
        return cls(dt.tm_year-1, floor(dt.tm_yday / 73), dt.tm_yday % 73 - 1, ss)


if __name__ == "__main__":
    print(SSTime.make(datetime.utcnow()))
