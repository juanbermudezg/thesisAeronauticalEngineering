#Created by @juanbermudezg trying to get his degree
#Date of last version: 05-02-2024 at 10:00pm in Ibagué-Tolima

import pandas as pd 

pathToFile = 'Fligthradar_database.xlsx'
df = pd.read_excel(pathToFile,'SKBO_Departures')
#df=df.drop(df[df['FLIGHT'].isna()].index)
print(df)