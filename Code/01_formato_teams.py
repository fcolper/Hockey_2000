import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

csv='Data_csv/Sobrepasado/TeamsMatches_2023-2024.csv'

df=pd.read_csv(csv)

# print(df.head())
# print(df.columns)
# print(df.dtypes)
# print(df.info())
# print(df.describe())

# colu=['gameId','gameType','gameDate','Team Home','Score Home','Score Away','Team Away',
#       'CF EV','CA EV', 'Shot Home EV','Shot Away EV','Goal Home EV','Goal Away EV','Miss Home EV',
#       'Miss Away EV','Block Home EV','Block Away EV','First Goal Home','First Goal Away','SOG Home','SOG Away',
#       'Faceoff Home','Faceoff Away','Pim Home','Pim Away']

df_group=df.copy()

# teams_nhl=['ANA', 'BOS', 'BUF', 'CAR', 'CBJ','CGY', 
#            'CHI', 'COL', 'DAL', 'DET', 'EDM', 'FLA', 
#            'LAK', 'MIN', 'MTL', 'NJD', 'NSH', 'NYI', 
#            'NYR', 'OTT', 'PHI', 'PIT', 'SJS', 'SEA',
#            'STL', 'TBL', 'TOR', 'UTA', 'VAN', 'VGK',
#            'WSH','WPG']

teams_nhl=list(df['Team Home'].unique())

lista_a=[]
for teams in teams_nhl:
    print('Equipo:',teams)
    df_home = df_group[df_group['Team Home'] == teams]
    #df_home.loc[:, 'Local/Visit']=1
    df_home['L_V'] = 1
    df_home=df_home.rename(columns={
        'Shot Home EV': 'Shot For EV',
        'Shot Away EV': 'Shot Against EV',
        'Score Home': 'Score_For',
        'Score Away': 'Score_Against',
        'Goal Home EV': 'Goal For EV',
        'Goal Away EV': 'Goal Against EV',
        'Miss Home EV': 'Miss For EV',
        'Miss Away EV': 'Miss Against EV',
        'Block Home EV': 'Block For EV',
        'Block Away EV': 'Block Against EV',
        'First Goal Home': 'First Goal For',
        'First Goal Away': 'First Goal Against',
        'SOG Home': 'SOG For',
        'SOG Away': 'SOG Against',
        'Faceoff Home': 'Faceoff For',
        'Faceoff Away': 'Faceoff Against',
        'Pim Home': 'Pim For',
        'Pim Away': 'Pim Against',
    })

    df_away = df_group[df_group['Team Away'] == teams]
    #df_away.loc[:, 'Local/Visit'] = 0
    df_away['L_V'] = 0
    df_away=df_away.rename(columns={
        'CF EV': 'CA EV',
        'CA EV': 'CF EV',
        'Score Home': 'Score_Against',
        'Score Away': 'Score_For',
        'Shot Home EV': 'Shot Against EV',
        'Shot Away EV': 'Shot For EV',
        'Goal Home EV': 'Goal Against EV',
        'Goal Away EV': 'Goal For EV',
        'Miss Home EV': 'Miss Against EV',
        'Miss Away EV': 'Miss For EV',
        'Block Home EV': 'Block Against EV',
        'Block Away EV': 'Block For EV',
        'First Goal Home': 'First Goal Against',
        'First Goal Away': 'First Goal For',
        'SOG Home': 'SOG Against',
        'SOG Away': 'SOG For',
        'Faceoff Home': 'Faceoff Against',
        'Faceoff Away': 'Faceoff For',
        'Pim Home': 'Pim Against',
        'Pim Away': 'Pim For',
    })

    df_home['W_L'] = df_home['Score_For'] - df_home['Score_Against']
    df_home['W_L'] = df_home['W_L'].apply(lambda x: 1 if x > 0 else 0)

    df_away['W_L'] = df_away['Score_Against'] - df_away['Score_For']
    df_away['W_L'] = df_away['W_L'].apply(lambda x: 1 if x < 0 else 0)

    df_team = pd.concat([df_home, df_away], ignore_index=False)

    df_completo=df_team.copy()

    # Crear la columna 'Oponente' y 'Team'
    df_completo['Oponente'] = df_completo.apply(lambda row: row['Team Away'] if row['Team Home'] == teams else (row['Team Home'] if row['Team Away'] == teams else None), axis=1)

    # Crear la columna 'Team' que muestra el equipo seleccionado
    df_completo['Team'] = df_completo.apply(lambda row: teams if row['Team Home'] == teams or row['Team Away'] == teams else None, axis=1)

    # Filtrar solo los partidos de 'TBL'
    tbl_games = df_completo[df_completo['Oponente'].notnull()]


    col=['gameId','gameType','gameDate','Team','Oponente','Score_For','Score_Against','W_L','L_V','Goal For EV','Goal Against EV','Shot For EV',
        'Miss For EV','Block For EV','Shot Against EV','Miss Against EV','Block Against EV',
        'First Goal For','SOG For','Faceoff For','Pim For','First Goal Against','SOG Against',
        'Faceoff Against','Pim Against']
    df_new=tbl_games[col]
    df_new.sort_index(ascending=True, inplace=True)
    lista_a.append(df_new)

combined_df = pd.concat(lista_a, axis=0, ignore_index=True)

#combined_df.rename(columns={'W/L': 'W_L'}, inplace=True)
#combined_df.rename(columns={'Local/Visit': 'L_V'}, inplace=True)

combined_df['gameDate'] = pd.to_datetime(combined_df['gameDate'])
combined_df["day_code"] = combined_df['gameDate'].dt.dayofweek
#combined_df["opp_code"] = combined_df["Oponente"].astype("category").cat.codes
combined_df["L_V"] = combined_df["L_V"].astype("category").cat.codes
#combined_df['Score_For']=combined_df['Score_For'].astype('int64')
#combined_df['Score_Against'].astype(int)

combined_df.columns = combined_df.columns.str.replace(' ', '_')

combined_df.to_csv(f'Data_csv/Test_TeamsMatches_2023-2024.csv', index=False)