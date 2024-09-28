import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

csv_2018='Data_csv/TeamsMatches_2018-2019.csv'
csv_2017='Data_csv/TeamsMatches_2017-2018.csv'
csv_2016='Data_csv/TeamsMatches_2016-2017.csv'
csv_2015='Data_csv/TeamsMatches_2015-2016.csv'
csv_2014='Data_csv/TeamsMatches_2014-2015.csv'
csv_2013='Data_csv/TeamsMatches_2013-2014.csv'
csv_2012='Data_csv/TeamsMatches_2012-2013.csv'
csv_2011='Data_csv/TeamsMatches_2011-2012.csv'
csv_2010='Data_csv/TeamsMatches_2010-2011.csv'
csv_2009='Data_csv/TeamsMatches_2009-2010.csv'
csv_2024='Data_csv/TeamsMatches_2019-2024.csv'

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
df_2018['Team'] = df_2018['Team'].replace(team_replacements)
df_2017['Team'] = df_2017['Team'].replace(team_replacements)
df_2016['Team'] = df_2016['Team'].replace(team_replacements)
df_2015['Team'] = df_2015['Team'].replace(team_replacements)
df_2014['Team'] = df_2014['Team'].replace(team_replacements)
df_2013['Team'] = df_2013['Team'].replace(team_replacements)
df_2012['Team'] = df_2012['Team'].replace(team_replacements)
df_2011['Team'] = df_2011['Team'].replace(team_replacements)
df_2010['Team'] = df_2010['Team'].replace(team_replacements)
df_2009['Team'] = df_2009['Team'].replace(team_replacements)

print('2018: ',df_2018['Team'].unique())
print('2017: ',df_2017['Team'].unique())
print('2016: ',df_2016['Team'].unique())
print('2015: ',df_2015['Team'].unique())
print('2014: ',df_2014['Team'].unique())
print('2013: ',df_2013['Team'].unique())
print('2012: ',df_2012['Team'].unique())
print('2011: ',df_2011['Team'].unique())
print('2010: ',df_2010['Team'].unique())
print('2009: ',df_2009['Team'].unique())

# Reemplazar los valores en la columna 'Team' del dataframe
df_2018['Oponente'] = df_2018['Oponente'].replace(team_replacements)
df_2017['Oponente'] = df_2017['Oponente'].replace(team_replacements)
df_2016['Oponente'] = df_2016['Oponente'].replace(team_replacements)
df_2015['Oponente'] = df_2015['Oponente'].replace(team_replacements)
df_2014['Oponente'] = df_2014['Oponente'].replace(team_replacements)
df_2013['Oponente'] = df_2013['Oponente'].replace(team_replacements)
df_2012['Oponente'] = df_2012['Oponente'].replace(team_replacements)
df_2011['Oponente'] = df_2011['Oponente'].replace(team_replacements)
df_2010['Oponente'] = df_2010['Oponente'].replace(team_replacements)
df_2009['Oponente'] = df_2009['Oponente'].replace(team_replacements)

print('2018: ',df_2018['Oponente'].unique())
print('2017: ',df_2017['Oponente'].unique())
print('2016: ',df_2016['Oponente'].unique())
print('2015: ',df_2015['Oponente'].unique())
print('2014: ',df_2014['Oponente'].unique())
print('2013: ',df_2013['Oponente'].unique())
print('2012: ',df_2012['Oponente'].unique())
print('2011: ',df_2011['Oponente'].unique())
print('2010: ',df_2010['Oponente'].unique())
print('2009: ',df_2009['Oponente'].unique())


# df_2020['Oponente'] = df_2020['Oponente'].replace(team_replacements)
# df_2021['Oponente'] = df_2021['Oponente'].replace(team_replacements)

# Contar los NaN en la columna 'Score_For'
nan_count = df_2009['Score_For'].isna().sum()
nan_count_2 = df_2009['Score_Against'].isna().sum()
print(f"Número de valores NaN en la columna 'Score_For': {nan_count}")
print(f"Número de valores NaN en la columna 'Score_Against': {nan_count_2}")

# Filtrar las filas donde la columna 'Score_For' tiene NaN
nan_rows = df_2009[df_2009['Score_For'].isna()]

# Mostrar los identificadores (id) de las filas con NaN
print(nan_rows[['gameId', 'Score_For']])


df=pd.concat([df_2024,df_2018,df_2017,df_2016,df_2015,df_2014,df_2013,df_2012,df_2011,df_2010,df_2009], ignore_index=True)

teams_nhl=list(df['Team'].unique())
teams_nhl=list(df['Oponente'].unique())

df.sort_values(by=['gameId'], inplace=True)
df.to_csv(f'Data_csv/TeamsMatches_2009-2024.csv', index=False)

# df.rename(columns={'W/L': 'W_L'}, inplace=True)
# df.rename(columns={'Local/Visit': 'L_V'}, inplace=True)
# df['Score_For'] = df['Score_For'].astype(int)
# df['Score_Against'] = df['Score_Against'].astype(int)

# df.to_csv(f'Data_csv/TeamsMatches_2019-2024.csv', index=False)
