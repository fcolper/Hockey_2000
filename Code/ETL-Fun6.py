import pandas as pd
import requests

# # Cargar los archivos CSV
# csv_2019='Data_csv/StatsPlayers_2023-2024_UNIQUE.csv'
# csv_2020='Data_csv/StatsPlayers_2022-2023.csv'
# csv_2021='Data_csv/StatsPlayers_2021-2022.csv'
# csv_2022='Data_csv/StatsPlayers_2020-2021.csv'
# csv_2023='Data_csv/StatsPlayers_2019-2020.csv'

# df_2019=pd.read_csv(csv_2019)
# df_2020=pd.read_csv(csv_2020)
# df_2021=pd.read_csv(csv_2021)
# df_2022=pd.read_csv(csv_2022)
# df_2023=pd.read_csv(csv_2023)



# resultado=pd.concat([df_2019,df_2020,df_2021,df_2022,df_2023], ignore_index=True)

# print(resultado.isnull().sum())

# resultado.to_csv('Data_csv/StatsPlayers_2019-2024.csv', index=False)

import requests
import pandas as pd

csv_total='Data_csv/StatsPlayers_2019-2024.csv'
df_total=pd.read_csv(csv_total)
filas_con_nulos_id = df_total[df_total['lastName'].isnull()]
print(filas_con_nulos_id)
print('2019-2024:',filas_con_nulos_id['id_skaters'].unique())


csv_total='Data_csv/StatsPlayers_2009-2024.csv'
df_total=pd.read_csv(csv_total)
filas_con_nulos_id = df_total[df_total['lastName'].isnull()]
print(filas_con_nulos_id)
print('2009-2024:',filas_con_nulos_id['id_skaters'].unique())

jugadores_faltantes=list(filas_con_nulos_id['id_skaters'].unique())
for l in jugadores_faltantes:
    print(l)
    url=f'https://api-web.nhle.com/v1/player/{l}/landing'
    response=requests.get(url)
    data_name = response.json()
    #print(data_name)
    name = data_name.get('firstName', {}).get('default', 'N/A')
    last_name = data_name.get('lastName', {}).get('default', 'N/A')
    df_total.loc[df_total['id_skaters'] == l, 'firstName'] = name
    df_total.loc[df_total['id_skaters'] == l, 'lastName'] = last_name
    print(name, last_name)


#df_total.to_csv('Data_csv/StatsPlayers_2009-2024_test.csv', index=False)



'''
################################

# Cargar los archivos CSV
csv_2019='Data_csv/CorsiStats_Players_2019-2020.csv'
csv_2020='Data_csv/CorsiStats_Players_2020-2021.csv'
csv_2021='Data_csv/CorsiStats_Players_2021-2022.csv'
csv_2022='Data_csv/CorsiStats_Players_2022-2023.csv'
csv_2023='Data_csv/CorsiStats_Players_2023-2024.csv'

id_players='Data_csv/Players_20002025.csv'
id_skaters=pd.read_csv(id_players)



df_2019=pd.read_csv(csv_2019)
df_2020=pd.read_csv(csv_2020)
df_2021=pd.read_csv(csv_2021)
df_2022=pd.read_csv(csv_2022)
df_2023=pd.read_csv(csv_2023)

nhl_players_season=list(df_2019['id_skaters'].unique())
large=len(nhl_players_season)
print('large:',large)

#Eliminar duplicados segun 'id
id_skaters=id_skaters.drop_duplicates(subset=['id'])
nhl_id_skaters=list(id_skaters['id'].unique())
large=len(nhl_id_skaters)
print('large:',large)

id_skaters = id_skaters.rename(columns={'id': 'id_skaters'})

col=['id_skaters','firstName','lastName']

#Quiero unir el id de los skaters con el id de los jugadores, agregando al dataframe de los jugadores las columnas firstname y lastname
resultado = pd.merge(df_2023, id_skaters[col], on='id_skaters', how='left')
resultado = resultado.rename(columns={'IdMatch': 'gameId'})
resultado['gameId']=resultado['gameId']+2023000000
print(df_2023)
print(resultado)

resultado.to_csv('Data_csv/Test_StatsPlayers_2023-2024.csv', index=False)

###################################################################################
'''



'''
list_name=[]
list_apellido=[]

for l in nhl_players_season:
    print(l)
    url=f'https://api-web.nhle.com/v1/player/{l}/landing'
    response = requests.get(url)
    data = response.json()
    data_name = response.json()
    name = data_name.get('firstName', {}).get('default', 'N/A')
    last_name = data_name.get('lastName', {}).get('default', 'N/A')
    list_name.append(name)
    list_apellido.append(last_name)

print(len(list_name), len(list_apellido))
'''


'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

csv_2018='Data_csv/StatsPlayers_2018-2019.csv'
csv_2017='Data_csv/StatsPlayers_2017-2018.csv'
csv_2016='Data_csv/StatsPlayers_2016-2017.csv'
csv_2015='Data_csv/StatsPlayers_2015-2016.csv'
csv_2014='Data_csv/StatsPlayers_2014-2015.csv'
csv_2013='Data_csv/StatsPlayers_2013-2014.csv'
csv_2012='Data_csv/StatsPlayers_2012-2013.csv'
csv_2011='Data_csv/StatsPlayers_2011-2012.csv'
csv_2010='Data_csv/StatsPlayers_2010-2011.csv'
csv_2009='Data_csv/StatsPlayers_2009-2010.csv'
csv_2024='Data_csv/StatsPlayers_2019-2024.csv'

df_2018=pd.read_csv(csv_2018)
df_2017=pd.read_csv(csv_2017)
df_2016=pd.read_csv(csv_2016)
df_2015=pd.read_csv(csv_2015)
df_2014=pd.read_csv(csv_2014)
df_2013=pd.read_csv(csv_2013)
df_2012=pd.read_csv(csv_2012)
df_2011=pd.read_csv(csv_2011)
df_2010=pd.read_csv(csv_2010)
df_2009=pd.read_csv(csv_2009)
df_2024=pd.read_csv(csv_2024)

# Crear un diccionario con las sustituciones que quieres hacer
team_replacements = {
    'T.B': 'TBL',
    'L.A': 'LAK',
    'N.J': 'NJD',
    'S.J': 'SJS'
}

# Reemplazar los valores en la columna 'Team' del dataframe
df_2018['team'] = df_2018['team'].replace(team_replacements)
df_2017['team'] = df_2017['team'].replace(team_replacements)
df_2016['team'] = df_2016['team'].replace(team_replacements)
df_2015['team'] = df_2015['team'].replace(team_replacements)
df_2014['team'] = df_2014['team'].replace(team_replacements)
df_2013['team'] = df_2013['team'].replace(team_replacements)
df_2012['team'] = df_2012['team'].replace(team_replacements)
df_2011['team'] = df_2011['team'].replace(team_replacements)
df_2010['team'] = df_2010['team'].replace(team_replacements)
df_2009['team'] = df_2009['team'].replace(team_replacements)



df=pd.concat([df_2024,df_2018,df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011,df_2010,df_2009], ignore_index=True)


df.sort_values(by=['gameId'], inplace=True)
df.to_csv(f'Data_csv/StatsPlayers_2009-2024.csv', index=False)
'''
