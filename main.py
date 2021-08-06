#!/usr/bin/python3

from datetime import datetime, timedelta, timezone
from math import floor


class SSTime(object):
    def __init__(self, year, month, date, ss):
        self.year = year
        self.month = month
        self.date = date
        self.ss = ss

    def __str__(self):
        ss = format(self.ss, "09,.2f").replace(",", "'")
        return f'{self.year}-{self.month}-{self.date} {ss}'

    @classmethod
    def make(cls, std_time: datetime):
        # TODO: use JS library, because this code is incorrect!
        dt = std_time.timetuple()
        hour = dt.tm_hour - 2
        if hour < 0:
            hour = 24 + hour
        ss = (hour * 3600 + dt.tm_min * 60 + dt.tm_sec)*(1000/864)
        return cls(year=dt.tm_year-1,
                   month=floor(dt.tm_yday / 73),
                   date=dt.tm_yday % 73 - 1,
                   ss=ss)


def compare(std_time: datetime, now=False):
    std_time_string = std_time.astimezone(tz=None).isoformat(sep=' ', timespec='seconds')
    print(f"{std_time_string}\t{'*' if now else '|'}\t{SSTime.make(std_time)}")


def delta(amount: int, unit: str):
    if unit == 'W':
        return timedelta(weeks=amount)
    if unit == 'D':
        return timedelta(days=amount)
    elif unit == 'h':
        return timedelta(hours=amount)
    elif unit == 'm':
        return timedelta(minutes=amount)
    elif unit == 's':
        return timedelta(seconds=amount)


if __name__ == "__main__":
    delta_amount = 1
    delta_unit = 'h'
    spread = 15

    base = datetime.utcnow().replace(tzinfo=timezone.utc)
    for i in range(-spread // 2, 0):
        compare(base + delta(delta_amount * i, delta_unit))
    compare(base, now=True)
    for i in range(1, spread // 2 + 1):
        compare(base + delta(delta_amount * i, delta_unit))
