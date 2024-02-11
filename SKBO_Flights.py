#Created by @juanbermudezg trying to get his degree
#Date of last version: 11-02-2024 at 01:03am in La Capilla - Boyacá

import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
import re
def extractContent(text:str)->str:
    matches = re.findall(r'\((.*?)\)', text)  # Encuentra el contenido dentro de paréntesis
    return matches[0] if matches else ''
def setFormatDay(dataF: pd.DataFrame, option:bool)->pd.DataFrame:
    if option:
        dataF["FULL_DATE"] = dataF['DATE'].map(str)+", 2024"+ " - " + dataF["TIME"].map(str)
        dataF = dataF.drop(['DATE', 'TIME'], axis=1)
        dataF = dataF.rename(columns={"FULL_DATE": "DATE"})
        dataF['DATE'] = pd.to_datetime(dataF['DATE'], format='%A, %b %d, %Y - %X', dayfirst=True)
        dataF['TO']=dataF['TO'].apply(extractContent)
        return dataF
    else:
        dataF["FULL_DATE"] = dataF['DATE'].map(str)+", 2024"+ " - " + dataF["TIME"].map(str)
        dataF = dataF.drop(['DATE', 'TIME'], axis=1)
        dataF = dataF.rename(columns={"FULL_DATE": "DATE"})
        dataF['DATE'] = pd.to_datetime(dataF['DATE'], format='%A, %b %d, %Y - %X', dayfirst=True)
        dataF['FROM']=dataF['FROM'].apply(extractContent)
        return dataF
def resetIndexCustom(dataF: pd.DataFrame)->pd.DataFrame:
        dataF = dataF.reset_index(drop=True)
        return dataF
def modifyDataFrame(dataF: pd.DataFrame, option:bool)->pd.DataFrame:
        dataF=resetIndexCustom(dataF)
        dataF = dataF[(dataF['STATUS'] != 'Canceled') & (dataF['STATUS'] != 'Unknown')]
        dataF=dataF.drop(dataF.index[len(dataF)-1])
        count=0
        days=[]
        dataF = resetIndexCustom(dataF)
        if option:
            for i in range(len(dataF['TO'])): 
                if pd.isna(dataF['TO'][i]):
                    count+=1
                    days.append(dataF['TIME'][i])
                else:
                    days.append(days[-1])
        else:
            for i in range(len(dataF['FROM'])): 
                if pd.isna(dataF['FROM'][i]):
                    count+=1
                    days.append(dataF['TIME'][i])
                else:
                    days.append(days[-1])
        dataF['DATE'] = days
        dataF=dataF.drop(dataF[dataF['FLIGHT'].isna()].index)
        dataF=setFormatDay(dataF, option)
        dataF=resetIndexCustom(dataF)
        return dataF
def saveDataFrame(dataF: pd.DataFrame, pathN: str, sheetN: str)->pd.DataFrame:
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
        workbook = xlsxwriter.Workbook(pathN)
        workbook.close()
        with pd.ExcelWriter(pathN, mode='a', engine='openpyxl') as writer:
            writer.book.remove(writer.book['Sheet1'])
            dataF.to_excel(writer, sheet_name=sheetN, index=False)
            print("Operation completed successfully!")
        return dataFLocal
def openDataFrame(oPathN: str, ePathN: str, sheetN: str, option:bool):
    df = pd.read_excel(oPathN,sheetN, index_col=False)
    df = modifyDataFrame(df, option)
    df=saveDataFrame(df,ePathN,sheetN)
    return df
def plotDataFrame(dataF: pd.DataFrame, text: str, textOption: bool)->None:
    plt.rcParams["font.family"] = "cursive"
    if textOption:
        dataF.TO.value_counts()[:10].sort_values().plot(kind = 'barh', color='Green', width = 0.5,)
        plt.title("Top 10 Departures from SKBO")
        widthGraph: int = (dataF['TO'].value_counts()[0]).item()
    else:
        dataF.FROM.value_counts()[:10].sort_values().plot(kind = 'barh', color='Red', width = 0.5,)
        plt.title("Top 10 Arrivals to SKBO")
        widthGraph: int = (dataF['FROM'].value_counts()[0]).item()
    plt.xlabel("Frequency in a determinate time")
    plt.ylabel("Destinations")
    plt.text((widthGraph*.75), 0, 'by @juanbermudezg', fontsize = 10)
    plt.savefig('src/topRoutesGraphs/SKBO/'+text+'.pdf')
    plt.show()
    plt.close()
def SKBODepartures()->None:
    df = openDataFrame('src\database\Fligthradar_database_raw.xlsx', 'src\database\Fligthradar_database.xlsx', 'SKBO_Departures', True)
    plotDataFrame(df, 'SKBO_Departures', True)
def SKBOArrivals()->None:
    df = openDataFrame('src\database\Fligthradar_database_raw.xlsx', 'src\database\Fligthradar_database.xlsx', 'SKBO_Arrivals', False)
    plotDataFrame(df, 'SKBO_Arrivals', False)
SKBOArrivals()
SKBODepartures()