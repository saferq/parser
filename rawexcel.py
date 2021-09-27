import pandas as pd
from pprint import pprint


df = pd.read_excel('ntd4 analys.xlsx', 'GOST0', header=0)

data = {
    'ntd': [],
    'ntd_name': [],
    'ntd_ntd': [],
}

for index, row in df.iterrows():
    print(row.ntd)
    n1 = df.ntd_old.str.contains(row.ntd).isin([True])
    n2 = df[n1]
    print(n2)
