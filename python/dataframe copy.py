import pandas as pd

DB_COL_LIST = [
    'status', 'region', 'country',
    'project_name', 'model_name', 'suffix', 'demand', 'spare', 'opportunity_code', 'vendor_code',
    'po', 'ex_factory', 'sp', 'sub_po', 'transport', 'etd', 'eta', 'bl', 'note'
]

ADDITIONAL_COL_LIST = [
    'created_by', 'created_at', 'corp', 'last_modified_by', 'last_modified_at', 'harmony', 'product_type'
]

ADDITIONAL_2 = ['err', 'err_col', 'msg', 'zip', 'address', 'assignee', 'watchers']


cols = ['status', 'region', 'country', 'project_name', 'po', 'ex_factory', 'harmony', 'err', 'err_col', 'msg']

data = [
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
    ['', None, pd.NA, pd.NaT, '2024-06-10', '2024-06-10', 'IDDX-123', 1, ['harmony', 'po'], 'errmsg~'],
]
data2 = [
    ['open', 'EU', 'Spain', 'project 4', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
    ['open', 'EU', 'Greece', 'project 5', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
]

df = pd.DataFrame(data=data, columns=cols)
print(' -- [0] df -- ')
print(df)

df2 = pd.DataFrame(data=data2, columns=cols)
print(' -- [1] df2 -- ')
print(df2)

print(' -- [2] Merge df + df2 -- ')
df_merged = pd.concat([df, df2]).reset_index(drop=True)
print(df_merged)

print(' -- [3] Null Value -- ')
row = df.iloc[2]
# print(row)
# print(row['status'], row['region'], row['country'], row['project_name'],)
# null_check = [row['status'], row['region'], row['country'], row['project_name']]
null_list = ['', None, pd.NA, pd.NaT]


def null_check(null_list: list):
    for v in null_list:
        if pd.isna(v) or v == '':  # 순서 중요
            print(f"{v} is Falsy")


null_check(null_list)


print(' -- [4] fillna -- ')
row = df.iloc[2]
print(df.fillna(''))
print(' -- ----- -- ')
print(df)

print(' -- [5] isna, isnull-- ')
print(pd.isna(''), pd.isnull(''))
print(pd.isna(None), pd.isnull(None))
print(pd.isna(pd.NA), pd.isnull(pd.NA))
print(pd.isna(pd.NaT), pd.isnull(pd.NaT))
