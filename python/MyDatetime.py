import os
import sys
# file이름 datetime.py 로 하면 ImportError날 수 있다.
from datetime import datetime, timedelta

current_date = datetime.now()
current_date_string = current_date.strftime("%Y-%m-%d")
one_year_before = current_date - timedelta(days=365)
one_year_before_string = one_year_before.strftime("%Y-%m-%d")
two_days_before = current_date - timedelta(days=2)
two_days_before_string = two_days_before.strftime("%Y-%m-%d")

print(type(current_date), current_date)
print(type(current_date_string), current_date_string)
print(type(one_year_before), one_year_before)
print(type(one_year_before_string), one_year_before_string)
print(type(two_days_before), two_days_before)
print(type(two_days_before_string), two_days_before_string)