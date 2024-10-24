# DAG - 'NBRM_OPPORTUNITY_DATA_TASK'

## query_opp
### get_data_from_gcp
### l1_preprocessing @@@ -> reset_index() x2
### orient_data_to_json
### change_update_state_to_all_false v
### send_json_to_es
### update_data_closedlost v

## query_opp_kibana
### get_data_from_gcp
### l1_preprocessing_dashboard @@@ -> reset_index() x3
### orient_data_to_json
### send_json_to_es

## query_opp_ILAMP
### get_data_from_gcp
### l1_preprocessing_ilamp @@@ -> reset_index() x2
### orient_data_to_json
### send_json_to_es

## query_opp_raw
### get_data_from_gcp
### orient_data_to_json
### send_json_to_es

## query_opp_item_raw
### get_data_from_gcp
### orient_data_to_json
### send_json_to_es


import pandas as pd

data = [[1, 'Alice', 23], [2, 'Bob', 25], [3, 'Charlie', 30]]
df = pd.DataFrame(data, columns=['ID', 'Name', 'Age'])
print(df)

data = {
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [23, 25, 30]
}
df = pd.DataFrame(data)
# print(df)
# # df.set_index('Name', inplace=True)
# df.reset_index(inplace=True)
# print(df)
# df.reset_index(inplace=True)
# print(df)
# df.reset_index(inplace=True)
# print(df.index)

arrays = [
    ['A', 'A', 'B', 'B'],
    ['one', 'two', 'one', 'two']
]
index = pd.MultiIndex.from_arrays(arrays, names=('first', 'second'))
data = {'value': [10, 20, 30, 40]}
df = pd.DataFrame(data, index=index)
print(df)
print(df.index)
df.reset_index(inplace=True)
print(df)
print(df.index)

data = {
    'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Value1': [10, 20, 30, 40, 50, 60],
    'Value2': [1, 2, 3, 4, 5, 6]
}

df = pd.DataFrame(data)
print(df)
grouped = df.groupby('Category')['Value1']  # ['A']
print(grouped.describe())
res = grouped.agg(list)
print(res)
print(res.index.names)
print('---')
print(df.columns.names)

data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
}
df = pd.DataFrame(data, index=['X', 'Y', 'Z'])

# Index 객체
index = df.index

# 속성
print("Index values:", index.values)
# print("Index name:", index.names)
print("Index dtype:", index.dtype)
print("Is index unique?:", index.is_unique)

# 메서드
# append
new_index = index.append(pd.Index(['W']))
print("Appended index:", new_index)

# delete
deleted_index = index.delete(1)
print("Deleted index:", deleted_index)

# drop
dropped_index = index.drop('Y')
print("Dropped index:", dropped_index)

# insert
inserted_index = index.insert(1, 'W')
print("Inserted index:", inserted_index)

# isin
isin_result = index.isin(['X', 'Z'])
print("Isin result:", isin_result)

# unique
unique_index = index.unique()
print("Unique index:", unique_index)

# duplicated
duplicated_index = index.duplicated()
print("Duplicated index:", duplicated_index)

# sort_values
sorted_index = index.sort_values()
print("Sorted index:", sorted_index)

# to_list
index_list = index.to_list()
print("Index as list:", index_list)