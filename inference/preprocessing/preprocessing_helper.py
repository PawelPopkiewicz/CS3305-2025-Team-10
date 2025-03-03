"""
Functions which are useful for preprocessing
"""

import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)

RUSH_HOURS = (("0800", "1100"), ("1500", "1800"))


def is_between_time(start_time, end_time, check_time):
    """Return true if check time is between times"""
    return start_time <= check_time <= end_time


def map_time_to_rush_hours(timestamp):
    """Maps times to categorical rush hours"""
    timestamp = int(timestamp)
    check_time = datetime.fromtimestamp(timestamp).strftime("%H%M")
    for start_time, end_time in RUSH_HOURS:
        if is_between_time(start_time, end_time, check_time):
            return True
    return False


def map_timestamp_to_minutes(timestamp):
    """Return the time in the day"""
    timestamp = int(timestamp)
    time = datetime.fromtimestamp(timestamp)
    minutes = time.hour*60 + time.minute + time.second/60
    return round(minutes, 1)


def parse_extended_strtime(time_str):
    """Parse times which can extend over 24 hours"""
    try:
        hours, minutes, seconds = map(int, time_str.split(':'))
    except ValueError:
        raise ValueError("Time string must be in HH:MM:SS format.")
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def map_strtime_to_timestamp(date, time_str):
    """Maps string datetime to a timestamp"""
    td = parse_extended_strtime(time_str)
    dt = datetime.strptime(date, "%Y%m%d")
    dt += td
    return dt.timestamp()


if __name__ == "__main__":
    pass


def map_date_to_weekday(date):
    """Maps dates to workday categorical"""
    return map_date_to_day(date) < 5


def map_date_to_day(date):
    """Returns the day in the week (0-6)"""
    return datetime.strptime(date, "%Y%m%d").weekday()


def calc_interpolation(dist_1, t_1, dist_2, t_2, stop_dist):
    """Calculates interpolation"""
    if None in [dist_1, t_1, dist_2, t_2]:
        return None

    if dist_2 > stop_dist >= dist_1:
        ratio = (stop_dist - dist_1) / (dist_2 - dist_1)
        stop_time = t_1 + (t_2 - t_1) * ratio
        return stop_time
    return None


def calc_speed(dist_1, t_1, dist_2, t_2):
    """Calculates the speed between two updates"""
    return abs(dist_1 - dist_2)/abs(t_1 - t_2)
