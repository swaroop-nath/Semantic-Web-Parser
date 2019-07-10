import pandas as pd

data_2 = pd.read_csv('First iteration Data\data_5.csv')

math_element_tags = ['mi', 'mo', 'mrow', 'mstyle', 'mfrac', 'msub', 'mtable', 'mtr', 'mtd', 'mn', 'mover', 'munder', 'msqrt', 'msup', 'mtext']
tag_dl_type = []
tag_math_type = []
tag_math_elem = []
tag_annotation = []

tag_names = data_2.name.values
print(len(tag_names))

for name in tag_names:
    tag_appends = {'dl': 'NO', 'math_type': 'NO', 'math_elem': 'NO', 'annot': 'NO'}
    if name == 'dl' or name == 'dd': tag_appends['dl'] = 'YES'
    if name == 'math' or name == 'semantics': tag_appends['math_type'] = 'YES'
    for math_elem in math_element_tags:
        if math_elem == name: tag_appends['math_elem'] = 'YES'
    if name == 'annotation': tag_appends['annot'] = 'YES'

    tag_dl_type.append(tag_appends['dl'])
    tag_math_type.append(tag_appends['math_type'])
    tag_math_elem.append(tag_appends['math_elem'])
    tag_annotation.append(tag_appends['annot'])

data = {'tag_dl_type': tag_dl_type, 'tag_math_type': tag_math_type, 'tag_math_elem': tag_math_elem, 'tag_annotation': tag_annotation}
df = pd.DataFrame(data)
writer = pd.ExcelWriter('First Iteration Data\data_2_i.xlsx', engine = 'openpyxl')
df.to_excel(writer, sheet_name = 'Sheet1', header = True)
writer.save()