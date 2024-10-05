import requests
import pandas as pd
'''
df=pd.read_csv(f'Data_csv/Test_Players_2023-2024.csv', sep=',')
print(df.columns)


# Función para obtener nombre y apellido a partir del ID
def obtener_nombre_apellido(number_id):
    url_player = f'https://api-web.nhle.com/v1/player/{number_id}/landing'
    try:
        response = requests.get(url_player)
        data_name = response.json()
        # Obtener los valores del JSON, asumiendo que la estructura es correcta
        name = data_name.get('firstName', {}).get('default', 'N/A')
        last_name = data_name.get('lastName', {}).get('default', 'N/A')
        return pd.Series([name, last_name])
    except Exception as e:
        print(f"Error al obtener datos para el ID {number_id}: {e}")
        return pd.Series(['N/A', 'N/A'])  # Valores por defecto si hay error

# Aplicar la función a cada fila del DataFrame y asignar a las nuevas columnas
df[['name', 'last_name']] = df['id_skaters'].apply(obtener_nombre_apellido)
column_names = ['IdMatch','gameType','team','id_skaters','name','last_name','position','sweaterNumber','goals','assists','points','pim','hits','shot','toi','shot_cf', 'miss_cf', 'block_cf', 'goal_cf', 'CF', 'shot_ca', 'miss_ca', 'block_ca', 'goal_ca', 'CA']
df=df.reindex(columns=column_names)

print(df.head())
df.to_csv("Data_csv/Test_Players_2023-2024.csv", index=False)
'''

# id_players='Data_csv/Players_20002023.csv'
# id_skaters=pd.read_csv(id_players)

# id_players_2='Data_csv/Players_20242025.csv'
# id_skaters_2=pd.read_csv(id_players_2)

# resultado=pd.concat([id_skaters,id_skaters_2], ignore_index=True)
# resultado=resultado.drop_duplicates(subset=['id'])
# resultado = resultado.drop(resultado.columns[0], axis=1)
# resultado.to_csv('Data_csv/Players_20002025.csv', index=False)

###########################################################################

# csv_2023='Data_csv/Test_Players_2023-2024.csv'
# csv_total='Data_csv/StatsPlayers_2023-2024.csv'

# df_2023=pd.read_csv(csv_2023)
# df_total=pd.read_csv(csv_total)

# df_combi=pd.concat([df_2023,df_total], ignore_index=True)
# df_combi.drop_duplicates(subset=['gameId'], inplace=True)


# csv_total='Data_csv/StatsPlayers_2023-2024.csv'

# df_combi=pd.read_csv(csv_total)
# df_combi.drop_duplicates(subset=['gameId'], inplace=True)
# df_combi.sort_values('gameId', inplace=True)
# df_combi.to_csv('Data_csv/StatsPlayers_2023-2024-Prueba.csv', index=False)

# # Cargar los datos desde el CSV
# df = pd.read_csv('Data_csv/StatsPlayers_2023-2024.csv')

# # Eliminar duplicados manteniendo la primera ocurrencia de cada id_skaters para cada gameId
# df_unique = df.groupby(['gameId', 'id_skaters']).first().reset_index()
# col=['gameId','gameType','team','id_skaters','position','sweaterNumber','goals','assists','points','pim','hits','shot','toi','shot_cf','miss_cf','block_cf','goal_cf','CF','shot_ca','miss_ca','block_ca','goal_ca','CA','firstName','lastName']
# df_unique=df_unique.reindex(columns=col)
# # Guardar el DataFrame resultante en un nuevo archivo CSV
# df_unique.to_csv('Data_csv/StatsPlayers_2023-2024_UNIQUE.csv', index=False)



# new_url=f'https://api-web.nhle.com/v1/gamecenter/2018020014/landing'

# response=requests.get(new_url)
# data=response.json()
# print(data['awayTeam']['abbrev'])

# archivo_base=pd.read_csv(f'Data_csv/TeamsMatches_2018-2019.csv', sep=',')
# archivo_base.sort_values('gameId', inplace=True)
# archivo_base.to_csv('Data_csv/TeamsMatches_2018-2019.csv', index=False)


# csv='Data_csv/Players_20002024_test.csv'
# csv_2025='Data_csv/Players_20242025_test.csv'

# df=pd.read_csv(csv)
# df_2025=pd.read_csv(csv_2025)

# df=pd.concat([df,df_2025], ignore_index=True)
# df.drop_duplicates(subset=['id'], inplace=True)
# df = df.drop(df.columns[0], axis=1)
# df.sort_values(by=['Season'], inplace=True)
# df.to_csv('Data_csv/Players_20002025_test.csv', index=False)

url='https://api-web.nhle.com/v1/schedule/2024-10-04' #Test
response=requests.get(url)
print(response)
data=response.json()
matches=data['gameWeek']
matches_2=matches[0]
print(len(matches_2))
date=data['gameWeek'][0]['date']
matches_2=matches[0]
print(len(matches_2['games']))
# new_df=pd.DataFrame(matches_2['games'])
# print(new_df.columns)
# new_df['Links']=new_df['id'].astype(str).str[-5:]
# new_df['gameDate']=date
# columnas=['id','season','Links','gameDate','gameType']
# playoff=new_df[columnas]
# print(playoff)


# new_url=f'https://api-web.nhle.com/v1/wsc/game-story/{l}'
# response=requests.get(new_url)
# data=response.json()
# #first_per=len(data['summary']['scoring'][0]['goals'])
# first_per=len(data['summary']['scoring'][0]['goals'])
# if first_per > 0:
#     first_goal_home=int(data['summary']['scoring'][0]['goals'][0]['homeScore'])
#     first_goal_away=int(data['summary']['scoring'][0]['goals'][0]['awayScore'])
# elif first_per == 0:
#     first_per=len(data['summary']['scoring'][1]['goals'])
#     if first_per > 0:
#         first_goal_home=int(data['summary']['scoring'][1]['goals'][0]['homeScore'])
#         first_goal_away=int(data['summary']['scoring'][1]['goals'][0]['awayScore'])
#     else:
#         first_per=len(data['summary']['scoring'][2]['goals'])
#         if first_per > 0:
#             first_goal_home=int(data['summary']['scoring'][2]['goals'][0]['homeScore'])
#             first_goal_away=int(data['summary']['scoring'][2]['goals'][0]['awayScore'])
#         else:
#             first_goal_home=0
#             first_goal_away=0

# sog_home=int(data['summary']['teamGameStats'][0]['homeValue'])
# sog_away=int(data['summary']['teamGameStats'][0]['awayValue'])
# face_home=float(data['summary']['teamGameStats'][1]['homeValue'])
# face_away=float(data['summary']['teamGameStats'][1]['awayValue'])
# pim_home=int(data['summary']['teamGameStats'][4]['homeValue'])
# pim_away=int(data['summary']['teamGameStats'][4]['awayValue'])
# hits_home=int(data['summary']['teamGameStats'][5]['homeValue'])
# hits_away=int(data['summary']['teamGameStats'][5]['awayValue'])
# #first_goal_home=int(data['summary']['scoring'][0]['goals'][0]['homeScore'])
# #first_goal_away=int(data['summary']['scoring'][0]['goals'][0]['awayScore'])
# face_home=float(data['summary']['teamGameStats'][1]['homeValue'])
# face_away=float(data['summary']['teamGameStats'][1]['awayValue'])
# pim_home=int(data['summary']['teamGameStats'][4]['homeValue'])
# pim_away=int(data['summary']['teamGameStats'][4]['awayValue'])
# hits_home=int(data['summary']['teamGameStats'][5]['homeValue'])
# hits_away=int(data['summary']['teamGameStats'][5]['awayValue']) 