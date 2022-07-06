from pandas import *

xls = ExcelFile("../school_db.xlsx")
df = xls.parse(xls.sheet_names[0])
print(df.transpose().to_dict())
