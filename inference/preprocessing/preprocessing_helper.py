"""
Functions which are useful for preprocessing
"""

import logging
from datetime import datetime

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


def map_date_to_weekday(date):
    """Maps dates to workday categorical"""
    dt = datetime.strptime(date, "%Y%m%d")
    return dt.weekday() < 5


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
