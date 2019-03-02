import time
from datetime import timedelta, datetime

import time_uuid
from dateutil.rrule import rrule, MONTHLY
from typing import List

from numpy import array_split


def generate_days(start_date, end_date) -> List[datetime]:
    days = []
    delta = end_date - start_date

    for i in range(delta.days + 1):
        day = start_date + timedelta(i)
        days.append(day)

    return days


def generate_months():
    now = datetime.now()
    last_known_date = datetime(2014, 1, 1,0, 0, 0)

    dates = [dt for dt in rrule(MONTHLY, dtstart=last_known_date, until=now)]
    dates_tuples = []

    for i, _ in enumerate(dates):
        if i % 2 is not 0:
            dates_tuples.append((dates[i], dates[i+1]))

    return dates_tuples


def create_uuid(date: datetime):
    timestamp = time.mktime(date.timetuple())
    return time_uuid.TimeUUID.with_timestamp(timestamp)
