from datetime import datetime, timedelta
import pandas as pd

cols = ['name', 'sp',]

data = [
    ['YYYYMMDD', '2025-01-01',],
    ['timestamp', '2021-02-02 08:23:42',],
    ['wrong date', '1999-01-41'],
    ['nullable', ''],
    ['nullable', '가'],
    ['nullable', pd.NA],
    ['nullable', pd.NaT],
    ['nullable', None],
]

df = pd.DataFrame(data=data, columns=cols)
# print(df)


def safe_date_conversion(date_str):
    try:
        date = pd.to_datetime(date_str).date()
        return date + timedelta(days=14)
    except:
        return None


df['precheck_due_date'] = df['sp'].apply(safe_date_conversion)
print(df)

##### pd.to_datetime

dl = ['2025-01-01', '2021-02-02 08:23:42', '1999-01-11', pd.NA, pd.NaT, None, '가']
for d in dl:
    try:
        dt = pd.to_datetime(d) + timedelta(days=14)  # .strftime('%Y-%m-%d')
        # print(type(dt), dt)
    except:
        print(f"cannot convert {d}")


##### format
today = datetime.now() + timedelta(days=14)  # .date().strftime('%Y-%m-%d')
print(today)
today = datetime.now().date() + timedelta(days=14)
print(today)
# today = datetime.now().date().strftime('%Y-%m-%d') + timedelta(days=14)
print(today)