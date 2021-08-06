#!/usr/bin/python3

import os
import sys
import json
from argparse import ArgumentParser
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
        time = format(self.time, "08,.1f").replace(",", "'")
        return f'{self.week_day} {self.year}-{self.month}-{self.day:02d} {time}'

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
    std_time_string = std_time.astimezone(tz=None).strftime('%w %Y-%m-%d %H:%M:%S')
    print(f"{std_time_string} {'*' if now else '|'} {SSTime.convert(std_time)}")


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
    parser = ArgumentParser(description='https://sssecond.com')
    parser.add_argument('step', nargs=1, help='Step size')
    parser.add_argument('unit',
                        nargs=1,
                        choices=['W', 'D', 'h', 'm', 's'],
                        help='Step unit (weeks, days, hours, minutes, seconds)')
    parser.add_argument('spread', nargs=1, help='Number of steps')
    config = parser.parse_args(sys.argv[1:])

    spread = int(config.spread[0])
    step = int(config.step[0])
    unit = config.unit[0]

    base = datetime.utcnow().replace(tzinfo=timezone.utc)
    for i in range(-spread // 2, 0):
        compare(base + delta(step * i, unit))
    compare(base, now=True)
    for i in range(1, spread // 2 + 1):
        compare(base + delta(step * i, unit))
