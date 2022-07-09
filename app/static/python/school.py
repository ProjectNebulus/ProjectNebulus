from pandas import *
def get_school():

    xls = ExcelFile("/app/static/school_db.xlsx")
    df = xls.parse(xls.sheet_names[0])
    # print(df.transpose().to_dict())
    schools = []
    df = df.transpose().to_dict()
    for i in range(0, len(df)):
        schools.append(
            [str(df[i]["Unnamed: 3"]) + "  (" + str(df[i]["Unnamed: 15"]) + ", " + str(df[i]["Unnamed: 16"]) + ")", i])
    # print(schools)
    return schools
