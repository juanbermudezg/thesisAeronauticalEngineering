#Created by @juanbermudezg trying to get his degree
#Date of last version: 06-02-2024 at 10:16am in Ibagué-Tolima

import pandas as pd

def resetIndexCustom(dataF):
    try:
        if dataF is None:
            return None
        if 'index' in dataF.columns:
            dataF = dataF.drop('index', axis=1)
        dataF = dataF.reset_index(drop=True)
        return dataF
    except:
        return dataF
def modifyDataFrame(dataF):
    try:
        dataF=resetIndexCustom(dataF)
        dataF = dataF[(dataF['STATUS'] != 'Canceled') & (dataF['STATUS'] != 'Unknown')]
        dataF=dataF.drop(dataF.index[len(dataF)-1])
        count=0
        days=[]
        dataF = resetIndexCustom(dataF)
        for i in range(len(dataF['FLIGHT'])): 
            if pd.isna(dataF['FLIGHT'][i]):
                count+=1
                days.append(dataF['TIME'][i])
            else:
                days.append(days[-1])
        dataF['DATE'] = days
        dataF=dataF.drop(dataF[dataF['FLIGHT'].isna()].index)
        dataF=resetIndexCustom(dataF)
        return dataF
    except:
        return dataF
def saveDataFrame(dataF, pathN, sheetN):
    dataFLocal=dataF
    try:
        with pd.ExcelWriter(pathN, mode='a', engine='openpyxl') as writer:
            try:
                dataF.to_excel(writer, sheet_name=sheetN, index=False)
                print("Operation completed successfully!")
            except Exception as e:
                if "already exists" in str(e):
                    writer.book.remove(writer.book[sheetN])
                    dataF.to_excel(writer, sheet_name=sheetN, index=False)
                    print("Operation completed successfully!")
                else:
                    raise e
        return dataFLocal              
    except:
        return dataFLocal
pathToFile = 'Fligthradar_database.xlsx'
sheetName = 'SKBO_Departures'
df = pd.read_excel(pathToFile,sheetName, index_col=False)
df = modifyDataFrame(df)
print(df)
df=saveDataFrame(df,pathToFile,sheetName)
