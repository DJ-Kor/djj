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
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 1, ['harmony', 'po'], 'errmsg~'],
]

data2 = [
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 0, [], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 1, ['status', 'po'], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 1, ['region', 'country'], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 1, ['country', 'po'], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10', 'IDDX-123', 1, ['harmony', 'po'], 'errmsg~'],
    ['closed', 'Asia', 'Korea', 'project 1', '2024-06-10', '2024-06-10',
        'IDDX-123', 1, ['country', 'project_name'], 'errmsg~'],
]

df = pd.DataFrame(data=data, columns=cols)
print(' -- [0] -- ')
print(df)

print(' -- [1] -- ')
print(df.reset_index(inplace=True))  # 'index' 생김
print(df)

print(' -- [2] -- ')
print(df.reset_index(inplace=True))  # 'level_0' 생김
print(df)

print(' -- [3] -- ')
print(df.reset_index(drop=True))  # Error
print(df)

print(' -- [4] -- ')
print(df.reset_index(inplace=True))
print(df)