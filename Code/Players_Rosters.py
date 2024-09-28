import requests
import pandas as pd

"""""

# path='Data_csv/AKA.csv'
# teams_csv=pd.read_csv(path)

teams=['ANA','BOS', 'BUF', 'CAR', 'CBJ','CGY', 
           'CHI', 'COL', 'DAL', 'DET', 'EDM', 'FLA', 
           'LAK', 'MIN', 'MTL', 'NJD', 'NSH', 'NYI', 
           'NYR', 'OTT', 'PHI', 'PIT', 'SJS', 'SEA',
           'STL', 'TBL', 'TOR', 'UTA', 'VAN', 'VGK',
           'WSH','WPG','ATL','PHX']

#SIN UTA
teams=['ANA','BOS', 'BUF', 'CAR', 'CBJ','CGY', 
           'CHI', 'COL', 'DAL', 'DET', 'EDM', 'FLA', 
           'LAK', 'MIN', 'MTL', 'NJD', 'NSH', 'NYI', 
           'NYR', 'OTT', 'PHI', 'PIT', 'SJS', 'SEA',
           'STL', 'TBL', 'TOR', 'VAN', 'VGK',
           'WSH','WPG','ATL','PHX']

positions=['forwards','defensemen','goalies']
years = list(range(2024, 2000, -1))
player_list=[]
for year in years:
    print(year)
    for team in teams:
        url=f'https://api-web.nhle.com/v1/roster/{team}/{year-1}{year}'
        response=requests.get(url)
        print(team)
        if response.status_code == 200:
            for position in positions:
                data=response.json()
                player=data[position]
                player_df=pd.DataFrame(player)
                #print(player_df.columns)
                player_df=player_df[['id', 'firstName', 'lastName', 'sweaterNumber',
                    'positionCode']]
                player_df['Team'] = team  # Añade una columna 'Team' al DataFrame con el valor del equipo actual
                player_df['Season'] = f'{year-1}{year}'  # Añade una columna 'Season' al DataFrame con el valor del año actual y el anterior como cadena
                # Reordena las columnas del DataFrame, colocando 'Team' y 'Season' al principio
                player_df = player_df[['Team', 'Season'] + [col for col in player_df.columns if col not in ['Team', 'Season']]]
                # Aplica una función lambda para obtener el valor 'default' de la columna 'firstName'
                player_df['firstName'] = player_df['firstName'].apply(lambda x: x['default'])

                # Aplica una función lambda para obtener el valor 'default' de la columna 'lastName'
                player_df['lastName'] = player_df['lastName'].apply(lambda x: x['default'])
                player_list.append(player_df)
        else:
            print(f"Error en la solicitud: {response.status_code}{url}") 
    print(year)      
Players_df = pd.concat(player_list, ignore_index=True)
Players_df['sweaterNumber'] = Players_df['sweaterNumber'].fillna(0)
Players_df['sweaterNumber'] = Players_df['sweaterNumber'].astype(int)
Players_df.to_csv('Data_csv/Players_20002024_test.csv')
"""



"""

archivo_csv=pd.read_csv('Data_csv/Players_20002025.csv')
df_1=pd.DataFrame(archivo_csv)
list_ids=df_1['id'].tolist()

# l=list_ids[0]
# url=f'https://api-web.nhle.com/v1/player/{l}/landing'
# response=requests.get(url)
# data=response.json()
# print(l,data['birthCity']['default'], data['birthCountry'])

player_data=[]
cont=0
for l in list_ids:
    cont+=1
    print(cont,l)
    url=f'https://api-web.nhle.com/v1/player/{l}/landing'
    response=requests.get(url)
    if response.status_code == 200:
        data=response.json()
        city = data.get('birthCity', {}).get('default', 'N/A')
        country = data.get('birthCountry', {})
        print(city, country)
        #guardar en un dataframe junto con l, city y country
        player_data.append({'id': l, 'city': city, 'country': country})
    else:
        print(f"Error en la solicitud: {response.status_code}{url}")

df = pd.DataFrame(player_data)
print(df.head())
df.to_csv('Data_csv/Ciudades_paises_players.csv')

df_merged = pd.merge(df_1, df, on='id', how='inner')

df_merged.to_csv('Data_csv/Players_20002025_test.csv', index=False)
"""
""""
for l in teams:
    url=f'https://api-web.nhle.com/v1/roster/{l}/20232024'
    response=requests.get(url)
    if response.status_code == 200:
        data=response.json()
        teams_stats=data['data']


    else:
        print(f"Error en la solicitud: {response.status_code}{url}")
"""
import matplotlib.pyplot as plt

csv='Data_csv/Players_20002024.csv'
df=pd.read_csv(csv)

# Agrupar por la columna 'city' y contar las ocurrencias
city_counts = df['city'].value_counts().head(20)

# Graficar las 20 ciudades más comunes
plt.figure(figsize=(10,6))
city_counts.plot(kind='bar')
plt.title('Top 20 Ciudades más Repetidas')
plt.xlabel('Ciudad')
plt.ylabel('Frecuencia')
plt.xticks(rotation=45)
plt.show()

# Agrupar por la columna 'city' y contar las ocurrencias
city_counts = df['country'].value_counts().head(20)

# Graficar las 20 ciudades más comunes
plt.figure(figsize=(10,6))
city_counts.plot(kind='bar')
plt.title('Top 20 Paises más Repetidas')
plt.xlabel('País')
plt.ylabel('Frecuencia')
plt.xticks(rotation=45)
plt.show()
