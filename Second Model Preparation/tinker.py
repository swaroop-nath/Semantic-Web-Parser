import pandas as pd

data_2 = pd.read_csv('First iteration Data\data_3.csv')

tag_elem = []

tag_names = data_2.name.values

for name in tag_names:
    tag_appends = 'NO'
    if name == 'td' or name == 'tr' or name == 'th':
        tag_appends = 'YES'
    tag_elem.append(tag_appends)

data = {'tag_elem': tag_elem}
df = pd.DataFrame(data)
writer = pd.ExcelWriter('First Iteration Data\data_2_i.xlsx', engine = 'openpyxl')
df.to_excel(writer, sheet_name = 'Sheet1', header = True)
writer.save()