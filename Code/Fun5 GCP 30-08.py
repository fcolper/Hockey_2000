import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

import requests
import pandas as pd
import json

# teams = []  # Crea una lista vacía llamada 'teams'
# client = storage.Client('poised-climate-416705')
# bucket = client.get_bucket('nhl-test-2')

# url_gsutil_corsi='gs://nhl-test-2/TeamsMatches_2024-2025.csv' #MODIFICAR 2024-2025

#archivo_base=pd.read_csv(url_gsutil_corsi, sep=',') #DESBLOQUEAR PARA LA SEASON GCP

#archivo_base=pd.read_csv(f'Data_csv/Test_teams_zero_GCP.csv', sep=',') #DESBLOQUEAR PARA LA SEASON
#url='https://api-web.nhle.com/v1/schedule/now'  #DESBLOQUEAR PARA LA SEASON GCP
url='https://api-web.nhle.com/v1/schedule/2024-09-23' #Test
response=requests.get(url)
print(response)
data=response.json()
matches=data['gameWeek']
matches_2=matches[0]
df=pd.DataFrame(matches_2)
#print(df.loc[3, 'games']['id'])
games_list=df['games'].tolist()
new_df=pd.DataFrame(games_list)
new_df['Links']=new_df['id'].astype(str).str[-5:]
new_df['gameDate']=df['date']
columnas=['id','season','Links','gameDate','gameType']
playoff=new_df[columnas]

large=playoff['id'].count()
print('large:',large)
id_matches_Links=playoff['Links']
print(id_matches_Links)
list_generalHome=[]
list_generalAway=[]
contador=0

for l in id_matches_Links:
    #print(l)
    url=f'https://www.nhl.com/scores/htmlreports/20242025/PL0{l}.HTM' #MODIFICAR 2024-2025
    gametype_fila=playoff['Links']==l
    gametype = int(playoff.loc[gametype_fila, 'gameType'].iat[0])
    # Realiza una solicitud para obtener el contenido HTML de la página
    response = requests.get(url)
    html_code = response.text

    soup = BeautifulSoup(html_code, 'html.parser')

    # Lista para almacenar todos los valores
    all_values_list = []

    # Find all the rows with class evenColor or oddColor
    filas = soup.find_all('tr', class_=['evenColor', 'oddColor'])

    for play in filas:
        # Extract data from each column
        play_data = play.find_all('td')

        # Check if play_data is not None before trying to find a table
        if play_data:
            # Extracting play information
            play_number = play_data[0].text
            period = play_data[1].text
            event_type = play_data[2].text
            time_info = play_data[3].text
            html_time = play_data[3]
            td_content = html_time.find('br')
            result_time = str(td_content.previous_sibling).strip()
            event_description = play_data[4].text
            additional_info = play_data[5].text

            # Check if additional_info is 'GOAL' and modify play_info class accordingly
            if event_description.strip() == 'GOAL':
                play_info = play.find('td', class_='bold + bborder + rborder')
            elif event_description.strip() == 'PENL':
                play_info = play.find('td', class_='italicize + bold + bborder + rborder')
            else:
                play_info = play.find('td', class_='+ bborder + rborder')

            # Variables para almacenar los valores actuales
            current_values = {
                'Play Number': play_number,
                'Period': period,
                'Event Type': event_type,
                'Time Info': result_time,
                'Event Description': event_description,
                'Additional Info': additional_info,
            }

            if play_info:
                table = play_info.find('table')
                # Check if table is not None and not empty
                if table and table.contents:
                    # Inicializar una lista para almacenar los números de los jugadores
                    numeros_jugadores = []

                    # Recorrer todas las filas de la primera tabla principal
                    for fila in table.find_all('tr'):
                        # Obtener la etiqueta <font> en la celda actual de la fila
                        font_tag = fila.find('font')
                        # Verificar si la etiqueta <font> está presente
                        if font_tag:
                            # Obtener el texto dentro de la etiqueta <font> (número del jugador)
                            numero_jugador = font_tag.get_text(strip=True)
                            numeros_jugadores.append(numero_jugador)
                            list_numeros_jugadores = [int(x) for x in numeros_jugadores]

                    # Añadir los valores a la lista general
                    current_values['awayTeam'] = list_numeros_jugadores[1:]
                else:
                    current_values['awayTeam'] = ''

            if event_description.strip() == 'GOAL':
                play_info = play.find('td', class_='bold + bborder')
            elif event_description.strip() == 'PENL':
                play_info = play.find('td', class_='italicize + bold + bborder')
            else:
                play_info = play.find_all('td', class_='+ bborder')

            if len(play_info) < 4:
                table = play_info.find('table')
                # Check if table is not None and not empty
                if table and table.contents:
                    # Inicializar una lista para almacenar los números de los jugadores
                    numeros_jugadores_home = []

                    # Recorrer todas las filas de la primera tabla principal
                    for fila in table.find_all('tr'):
                        # Obtener la etiqueta <font> en la celda actual de la fila
                        font_tag = fila.find('font')
                        # Verificar si la etiqueta <font> está presente
                        if font_tag:
                            # Obtener el texto dentro de la etiqueta <font> (número del jugador)
                            numero_jugador_home = font_tag.get_text(strip=True)
                            numeros_jugadores_home.append(numero_jugador_home)

                    list_numeros_jugadores_home = [int(x) for x in numeros_jugadores_home]
                    # Añadir los valores a la lista general
                    current_values['homeTeam'] = list_numeros_jugadores_home[1:]
                else:
                    current_values['homeTeam'] = ''
            else:
                table = play_info[6].find('table')
                # Check if table is not None and not empty
                if table and table.contents:
                    # Inicializar una lista para almacenar los números de los jugadores
                    numeros_jugadores_home = []

                    # Recorrer todas las filas de la primera tabla principal
                    for fila in table.find_all('tr'):
                        # Obtener la etiqueta <font> en la celda actual de la fila
                        font_tag = fila.find('font')
                        # Verificar si la etiqueta <font> está presente
                        if font_tag:
                            # Obtener el texto dentro de la etiqueta <font> (número del jugador)
                            numero_jugador_home = font_tag.get_text(strip=True)
                            numeros_jugadores_home.append(numero_jugador_home)
                            list_numeros_jugadores_home = [int(x) for x in numeros_jugadores_home]

                    # Añadir los valores a la lista general
                    current_values['homeTeam'] = list_numeros_jugadores_home[1:]
                else:
                    current_values['homeTeam'] = ''

            # Añadir el conjunto actual de valores a la lista general
            all_values_list.append(current_values)
    #print(all_values_list)

    #Imprimir la lista completa de valores al final
    #print(all_values_list)
    #for l in all_values_list:
    #    print(l)

    columnas=soup.find_all('td',class_=['heading + bborder'])
    #print(len(columnas))
    cont=0
    list_columnas=[]
    for colum in columnas:
        cont=cont+1
        #print(colum.text)
        list_columnas.append(colum.text)
        if cont >7:
            break
    if len(list_columnas) <1:
        break
    AKA_away_team = list_columnas[6].split()[0] 
    AKA_home_team = list_columnas[7].split()[0] 

    df=pd.DataFrame(all_values_list)
    df.columns=list_columnas


    df['Team']=df['Description'].str.slice(0,3)

    #print(df)

    df_home=df[df['Team']== AKA_home_team]
    df_home_EV=df_home[df_home['Str']=='EV']
    df_home_EV_Shot=df_home_EV[df_home_EV['Event']=='SHOT']
    #print('df_home_EV_Shot:', df_home_EV_Shot)
    df_home_EV_Goal=df_home_EV[df_home_EV['Event']=='GOAL']
    #print('df_home_EV_Goal:', df_home_EV_Goal)
    #print(df_home_EV_Shot)
    corsifor_shot_EV=len(df_home_EV_Shot)
    corsifor_goal_EV=len(df_home_EV_Goal)
    #print(len(df_home_EV_Shot))
    df_home_EV=df_home[df_home['Str']=='EV']
    df_home_EV_Miss=df_home_EV[df_home_EV['Event']=='MISS']
    #print(df_home_EV_Miss)
    corsifor_miss_EV=len(df_home_EV_Miss)
    #print(len(df_home_EV_Miss))
    df_home_EV=df_home[df_home['Str']=='EV']
    df_home_EV_Block=df_home_EV[df_home_EV['Event']=='BLOCK']
    #print(df_home_EV_Block)
    corsifor_block_EV=len(df_home_EV_Block)
    corsifor_total=corsifor_shot_EV+corsifor_miss_EV+corsifor_block_EV+corsifor_goal_EV
    #print(df_home_EV_Block)
    #print(len(df_home_EV_Block))
    #print(AKA_home_team,'Corsi For_EV:',corsifor_total)

    df_away=df[df['Team']== AKA_away_team]
    df_away_EV=df_away[df_away['Str']=='EV']
    df_away_EV_Shot=df_away_EV[df_away_EV['Event']=='SHOT']
    df_away_EV_Goal=df_away_EV[df_away_EV['Event']=='GOAL']
    corsiag_shot_EV=len(df_away_EV_Shot)
    corsiag_goal_EV=len(df_away_EV_Goal)

    #print(df_away_EV_Shot)
    #print(len(df_away_EV_Shot))

    df_away_EV=df_away[df_away['Str']=='EV']
    df_away_EV_Miss=df_away_EV[df_away_EV['Event']=='MISS']
    corsiag_miss_EV=len(df_away_EV_Miss)

    #print(df_away_EV_Miss)
    #print(len(df_away_EV_Miss))

    df_away_EV=df_away[df_away['Str']=='EV']
    df_away_EV_Block=df_away_EV[df_away_EV['Event']=='BLOCK']
    #print(df_away_EV_Block)
    corsiag_block_EV=len(df_away_EV_Block)

    corsiag_total=corsiag_shot_EV+corsiag_miss_EV+corsiag_block_EV+corsiag_goal_EV
    #print(df_away_EV_Block)
    #print(len(df_away_EV_Block))
    #print(AKA_home_team,'Corsi Against:',corsiag_total)

    df_filtrado = df.loc[(df[list_columnas[6]].apply(len) == 6) & (df[list_columnas[7]].apply(len) == 6)]

    #print(df_filtrado)
    df_5v5_ANA=df_filtrado[df_filtrado['Team']== AKA_home_team]
    #print(df_5v5_ANA)
    df_5v5_ANA_shots=df_5v5_ANA[df_5v5_ANA['Event']=='SHOT']
    df_5v5_ANA_goal=df_5v5_ANA[df_5v5_ANA['Event']=='GOAL']
    #print(df_5v5_ANA_shots)
    #print(len(df_5v5_ANA_shots))
    df_5v5_ANA_miss=df_5v5_ANA[df_5v5_ANA['Event']=='MISS']
    #print(df_5v5_ANA_miss)
    #print(len(df_5v5_ANA_miss))
    df_5v5_ANA_block=df_5v5_ANA[df_5v5_ANA['Event']=='BLOCK']
    #print(df_5v5_ANA_block)
    #print(len(df_5v5_ANA_block))
    corsifor_shot_5v5=len(df_5v5_ANA_shots)
    corsifor_goal_5v5=len(df_5v5_ANA_goal)
    corsifor_miss_5v5=len(df_5v5_ANA_miss)
    corsifor_block_5v5=len(df_5v5_ANA_block)

    corsifor_ANA_5v5=len(df_5v5_ANA_shots)+len(df_5v5_ANA_miss)+len(df_5v5_ANA_block)+len(df_5v5_ANA_goal)
    #print(AKA_home_team,'CorsiFor 5v5:',corsifor_ANA_5v5)

    df_5v5_TOR=df_filtrado[df_filtrado['Team']==AKA_away_team]
    #print(df_5v5_TOR)
    df_5v5_TOR_shots=df_5v5_TOR[df_5v5_TOR['Event']=='SHOT']
    df_5v5_TOR_goal=df_5v5_TOR[df_5v5_TOR['Event']=='GOAL']
    #print(df_5v5_TOR_shots)
    #print(len(df_5v5_TOR_shots))
    df_5v5_TOR_miss=df_5v5_TOR[df_5v5_TOR['Event']=='MISS']
    #print(df_5v5_TOR_miss)
    #print(len(df_5v5_TOR_miss))
    df_5v5_TOR_block=df_5v5_TOR[df_5v5_TOR['Event']=='BLOCK']
    #print(df_5v5_TOR_block)
    #print(len(df_5v5_TOR_block))
    corsiag_shot_5v5=len(df_5v5_TOR_shots)
    corsiag_goal_5v5=len(df_5v5_TOR_goal)
    corsiag_miss_5v5=len(df_5v5_TOR_miss)
    corsiag_block_5v5=len(df_5v5_TOR_block)

    corsifor_TOR_5v5=len(df_5v5_TOR_shots)+len(df_5v5_TOR_miss)+len(df_5v5_TOR_block)+len(df_5v5_TOR_goal)
    #print(AKA_home_team,'CorsiAgainst 5v5:',corsifor_TOR_5v5)

    score=soup.find_all('td', style='font-size: 40px;font-weight:bold')

    away_Score=score[0].text
    home_Score=score[1].text

    #print('Score',AKA_away_team,':',away_Score)
    #print('Score', AKA_home_team,':',home_Score)

    fila_buscar = playoff.loc[playoff['Links'] == l]
    #print('fila buscar', fila_buscar)
    match_id=fila_buscar['id'].values[0]
    fecha_game=fila_buscar['gameDate'].values[0]
    fecha_str = str(fecha_game)
    fecha_game = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S.%f000').strftime('%Y-%m-%d') if '.' in fecha_str else fecha_str
    new_url=f'https://api-web.nhle.com/v1/gamecenter/20230{l}/landing' #Cambiar a 2024 si la season es 2024-2025
    response=requests.get(new_url)
    data=response.json()
    #first_per=len(data['summary']['scoring'][0]['goals'])
    first_per=len(data['summary']['scoring'][0]['goals'])
    if first_per > 0:
        first_goal_home=int(data['summary']['scoring'][0]['goals'][0]['homeScore'])
        first_goal_away=int(data['summary']['scoring'][0]['goals'][0]['awayScore'])
    elif first_per == 0:
        first_per=len(data['summary']['scoring'][1]['goals'])
        if first_per > 0:
            first_goal_home=int(data['summary']['scoring'][1]['goals'][0]['homeScore'])
            first_goal_away=int(data['summary']['scoring'][1]['goals'][0]['awayScore'])
        else:
            first_per=len(data['summary']['scoring'][2]['goals'])
            if first_per > 0:
                first_goal_home=int(data['summary']['scoring'][2]['goals'][0]['homeScore'])
                first_goal_away=int(data['summary']['scoring'][2]['goals'][0]['awayScore'])
            else:
                first_goal_home=0
                first_goal_away=0

    sog_home=int(data['summary']['teamGameStats'][0]['homeValue'])
    sog_away=int(data['summary']['teamGameStats'][0]['awayValue'])
    face_home=float(data['summary']['teamGameStats'][1]['homeValue'])
    face_away=float(data['summary']['teamGameStats'][1]['awayValue'])
    pim_home=int(data['summary']['teamGameStats'][4]['homeValue'])
    pim_away=int(data['summary']['teamGameStats'][4]['awayValue'])
    hits_home=int(data['summary']['teamGameStats'][5]['homeValue'])
    hits_away=int(data['summary']['teamGameStats'][5]['awayValue'])
    #first_goal_home=int(data['summary']['scoring'][0]['goals'][0]['homeScore'])
    #first_goal_away=int(data['summary']['scoring'][0]['goals'][0]['awayScore'])
    face_home=float(data['summary']['teamGameStats'][1]['homeValue'])
    face_away=float(data['summary']['teamGameStats'][1]['awayValue'])
    pim_home=int(data['summary']['teamGameStats'][4]['homeValue'])
    pim_away=int(data['summary']['teamGameStats'][4]['awayValue'])
    hits_home=int(data['summary']['teamGameStats'][5]['homeValue'])
    hits_away=int(data['summary']['teamGameStats'][5]['awayValue']) 
                
    diccionario_TEAM={
        'gameId':match_id,
        'gameDate':fecha_game,
        'gameType':gametype,
        'Team': AKA_home_team,
        'Score_For':home_Score,
        'Score_Against': away_Score,
        'Oponente': AKA_away_team,
        'First Goal Home':first_goal_home,
        'First Goal Away':first_goal_away,
        'SOG Home':sog_home,
        'SOG Away':sog_away,
        'Faceoff Home':face_home,
        'Faceoff Away':face_away,
        'Pim Home':pim_home,
        'Pim Away':pim_away,
        'Shot Home EV':corsifor_shot_EV,
        'Miss Home EV':corsifor_miss_EV,
        'Block Home EV':corsifor_block_EV,
        'Goal Home EV': corsifor_goal_EV,
        'CF EV': corsifor_total,
        'Shot Away EV':corsiag_shot_EV,
        'Miss Away EV':corsiag_miss_EV,
        'Block Away EV':corsiag_block_EV,
        'Goal Away EV': corsiag_goal_EV,              
        'CA EV': corsiag_total
        #'Shot Home 5v5':corsifor_shot_5v5,
        #'Miss Home 5v5':corsifor_miss_5v5,
        #'Block Home 5v5':corsifor_block_5v5, 
        #'Goal Home 5V5':corsifor_goal_5v5,               
        #'CF 5v5': corsifor_ANA_5v5,
        #'Shot Away 5v5':corsiag_shot_5v5,
        #'Miss Away 5v5':corsiag_miss_5v5,
        #'Block Away 5v5':corsiag_block_5v5,
        #'Goal Away 5v5':corsiag_goal_5v5,
        #'CA 5v5':  corsifor_TOR_5v5
    }
    list_generalHome.append(diccionario_TEAM)

    #print(contador)
    if contador >=large-1:
        break
    contador=contador+1
    print(f'Quedan: ', len(id_matches_Links) - contador )
df_total_final=pd.DataFrame(list_generalHome)
# eliminar_fila_index=0
#archivo_base['gameDate'] = pd.to_datetime(archivo_base['gameDate'])
#df_total_final=pd.concat([archivo_base,df_total_final], ignore_index=True)

# CorsiTeam_TBL_Uptdate=CorsiTeam_TBL_Uptdate.drop_duplicates(subset='gameId')
# CorsiTeam_TBL_Uptdate=CorsiTeam_TBL_Uptdate.sort_values('gameDate')
#archivo_base['gameDate'] = pd.to_datetime(archivo_base['gameDate'])

df_total_final['Score_For']=df_total_final['Score_For'].astype(int)
df_total_final['Score_Against']=df_total_final['Score_Against'].astype(int)

df_group=df_total_final.copy()
teams_nhl=list(df_group['Team'].unique())

lista_a=[]
for teams in teams_nhl:
    #if teams != 'UTA':
    df_home = df_group[df_group['Team'] == teams]
    df_home = df_home.reset_index(drop=True)
    #df_home.loc[:, 'Local/Visit']=1
    df_home['L_V'] = 1
    df_home=df_home.rename(columns={
        'Shot Home EV': 'Shot For EV',
        'Shot Away EV': 'Shot Against EV',
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

    df_away = df_group[df_group['Team'] == teams]
    df_away = df_away.reset_index(drop=True)
    #df_away.loc[:, 'Local/Visit'] = 0
    df_away['L_V'] = 0
    df_away=df_away.rename(columns={
        'Team':'Oponente',
        'Oponente':'Team',
        'CF EV': 'CA EV',
        'CA EV': 'CF EV',
        'Score_For': 'Score_Against',
        'Score_Against': 'Score_For',
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

    # df_home['W_L'] = df_home['Score_For'] - df_home['Score_Against']
    # df_home['W_L'] = df_home['W_L'].apply(lambda x: 1 if x > 0 else 0)

    # df_away['W_L'] = df_away['Score_For'] - df_away['Score_Against']
    # df_away['W_L'] = df_away['W_L'].apply(lambda x: 1 if x < 0 else 0)

    df_team = pd.concat([df_home, df_away], ignore_index=False)
    print('DF_home:',df_home)
    print('DF_away:',df_away)
    df_completo=df_team.copy()

    # Crear la columna 'Oponente' y 'Team'
    #df_completo['Oponente'] = df_completo.apply(lambda row: row['Oponente'] if row['Team'] == teams else (row['Team'] if row['Oponente'] == teams else None), axis=1)

    # Crear la columna 'Team' que muestra el equipo seleccionado
    #df_completo['Team'] = df_completo.apply(lambda row: teams if row['Team'] == teams or row['Oponente'] == teams else None, axis=1)

    # Filtrar solo los partidos de 'TBL'
    tbl_games = df_completo[df_completo['Oponente'].notnull()]
    tbl_games['W_L'] = tbl_games['Score_For'] - tbl_games['Score_Against']
    tbl_games['W_L'] = tbl_games['W_L'].apply(lambda x: 1 if x > 0 else 0)

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
#archivo_base['gameDate'] = pd.to_datetime(archivo_base['gameDate']) #DESBLOQUEAR PARA LA SEASON

combined_df["day_code"] = combined_df['gameDate'].dt.dayofweek
#combined_df["opp_code"] = combined_df["Oponente"].astype("category").cat.codes
combined_df["L_V"] = combined_df["L_V"].astype("category").cat.codes

combined_df.columns = combined_df.columns.str.replace(' ', '_')
combined_df.to_csv(f'Data_csv/TeamsMatches_2024-2025_test.csv', index=False) #PRIMER ARCHIVO

#new_teams_season=pd.concat([archivo_base,combined_df], ignore_index=True) #DESBLOQUEAR PARA LA SEASON

#new_teams_season.to_csv(url_gsutil_corsi, index=False) #DESBLOQUEAR PARA LA SEASON GCP

#new_teams_season.to_csv(f'Data_csv/TeamsMatches_2024-2025_test.csv', index=False) #DESBLOQUEAR PARA LA SEASON