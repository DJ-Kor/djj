import os
import sys
# file이름 datetime.py 로 하면 ImportError날 수 있다.
from datetime import datetime, timedelta

# now
current = datetime.now()  # datetime.datetime
print(type(current), current)

# timedelta
one_year_before = current - timedelta(days=365)  # datetime.datetime
print(type(one_year_before), one_year_before)
two_days_before = current - timedelta(days=2)
print(type(two_days_before), two_days_before)

# strftime
ymd = current.strftime("%Y-%m-%d")  # str
print(type(ymd), ymd)  # YYYY-MM-DD 2024-07-23


# ISOCALENDER
iso = current.isocalendar()  # tuple
print(type(iso), iso)  # (2024, 30, 2)