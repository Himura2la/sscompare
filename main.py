#!/usr/bin/python3

import os
import json
from math import floor
from datetime import datetime, timedelta, timezone
from subprocess import check_output

convert_ss_path = os.path.join(os.path.split(__file__)[0], 'convert_ss.js')


class SSTime(object):
    def __init__(self, year, month, day, time, week=None, week_day=None):
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.week = week
        self.week_day = week_day

    def __str__(self):
        time = format(self.time, "09,.2f").replace(",", "'")
        return f'{self.year}-{self.month}-{self.day} {time}'

    @classmethod
    def convert(cls, std_time: datetime):
        js_timestamp = round(std_time.timestamp() * 1000)
        lib_response = check_output(['node', convert_ss_path, str(js_timestamp)])
        ss = json.loads(lib_response.decode())
        return cls(
            year=ss['year'],
            month=ss['month'],
            day=ss['day'],
            time=ss['time'],
            week=ss['week'],
            week_day=ss['week_day']
        )


def compare(std_time: datetime, now=False):
    std_time_string = std_time.astimezone(tz=None).isoformat(sep=' ', timespec='seconds')
    print(f"{std_time_string}\t{'*' if now else '|'}\t{SSTime.convert(std_time)}")


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
