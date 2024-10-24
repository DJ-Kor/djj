import pandas as pd

data = [[1, 'Alice', 23], [2, 'Bob', 25], [3, 'Charlie', 30]]
df = pd.DataFrame(data, columns=['ID', 'Name', '인덱스'], index=['가', '나', '다'])
print(df)
df.index.set_names('인덱스', inplace=True)
# df.reset_index(inplace=True)
print(df)

print('------')
data = {
    'ID': [1, 2, 3],
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [23, 25, 30]
}
df2 = pd.DataFrame(data)
print(df2)

print('------')
arrays = [
    ['A', 'A', 'B', 'B'],
    ['one', 'two', 'one', 'two']
]
index = pd.MultiIndex.from_arrays(arrays, names=('first', 'second'))
data = {'value': [10, 20, 30, 40]}
df3 = pd.DataFrame(data, index=index)
print(df3)

print('------')
data = {
    'Category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Value1': [10, 20, 30, 40, 50, 60],
    'Value2': [1, 2, 3, 4, 5, 6]
}
df4 = pd.DataFrame(data)
print(df4)
grouped = df4.groupby('Category')  # ['Value1']
print(grouped.describe())
res = grouped.agg(list)
print(res)
print(res.columns)

print('--------------------------------------------')


def safe_reset_index(df):
    if isinstance(df, pd.Series):
        return df.reset_index()
    idx = df.index.names
    if idx == [None]:
        print('idx = none')
        idx = ['index']
    col = df.columns.values
    print(idx)
    print(col)

    for i in idx:
        if i in col:
            print(f"{i} in columns !")

            df.reset_index(drop=True, inplace=True)
            break

    else:
        print('no idx dup in col')
        df.reset_index(inplace=True)

    return df


# for d in [df, df2, df3, df4]:
    # print(safe_reset_index(d))
    # print('-=-=-===-=-=-=-=-=-=-=-=-=')

d = df
dd = d.reset_index(drop=True)
ddd = dd.reset_index()
dddd = ddd.reset_index()

for this in [d, dd, ddd, dddd]:
    print(safe_reset_index(this))
    print('-=-=-===-=-=-=-=-=-=-=-=-=')


s = pd.Series(data=['a', 'b', 'c'])
ss = pd.Series(data=['가', '나', '다'])

abc = s.reset_index()
print(abc)

print(safe_reset_index(s))
print(safe_reset_index(ss))

ed = pd.DataFrame(columns=['가'])
print(ed)
if ed.empty:
    print('empty data frame is not empty')


def test():
    a = []
    if not a:
        print('not a')
        exit()


test()