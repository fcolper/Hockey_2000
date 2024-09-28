from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import re

url='https://api-web.nhle.com/v1/schedule/2024-02-23'
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
final_list=[]
quedan=large

# Función para convertir una cadena de texto en una lista de números
def convertir_a_lista(elemento):
    # Verificar si el elemento ya es una lista
    if isinstance(elemento, list):
        return elemento
    else:
        # Usar una expresión regular para encontrar todos los números en la cadena
        numeros = re.findall(r'\d+', elemento)
        # Convertir los números encontrados a enteros y retornar la lista
        return [int(num) for num in numeros]
quedan=len(id_matches_Links)
for l in id_matches_Links:
    print(l)
    print('Quedan:',quedan)
    gametype_fila=playoff['Links']==l
    gametype = int(playoff.loc[gametype_fila, 'gameType'].iat[0])
    idMatch_fila=int(playoff.loc[gametype_fila, 'id'].iat[0])#############ESTO ES NUEVOO#############
    quedan=quedan-1
    url=f'https://www.nhl.com/scores/htmlreports/20232024/PL0{l}.HTM' #MODIFICAR SEASON
    # Especifica la URL que deseas analizar
    #url_html = 'https://www.nhl.com/scores/htmlreports/20232024/PL020001.HTM'

    # Realiza una solicitud para obtener el contenido HTML de la página
    response = requests.get(url)
    html_code = response.text

    soup = BeautifulSoup(html_code, 'html.parser')

    # Lista para almacenar todos los valores
    all_values_list = []

    def skaters_(url):
        boxscore=requests.get(url)
        data=boxscore.json()
        #print(data)
        #data_player=data['boxscore']['playerByGameStats']
        data_player=data['playerByGameStats']
        #data_away=data_player['awayTeam']
        #data_home=data_player['homeTeam']
        positions=['forwards','defense']
        teams=['awayTeam','homeTeam']
        list_datapos=[]
        df_general=pd.DataFrame()
        for team in teams:
            data_team=data_player[team]
            team_awayhome=data[team]['abbrev']
            #print(team_awayhome)
            for pos in positions:
                data_positions=data_team[pos]
                player_df=pd.DataFrame(data_positions)
                player_df['Team'] = team_awayhome
                player_df = player_df[['Team'] + [col for col in player_df.columns if col not in ['Team']]]
                list_datapos.append(player_df)
                #df_general=pd.concat(list, ignore_index=True)

        df_concat = pd.concat(list_datapos, ignore_index=True)
        return df_concat
    
    skaters=skaters_(f'https://api-web.nhle.com/v1/gamecenter/20230{l}/boxscore') #MODIFICAR EL AÑO

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

    #print(list_columas)

    #print(all_values_list[321])

    df=pd.DataFrame(all_values_list)
    df.columns=list_columnas
    #print('DF: ', df)

    #print(df['TBL On Ice'])

    df['Team']=df['Description'].str.slice(0,3)
    #df.to_csv('Data_csv/Matches_TBL_2023-2024-PRUEBA.csv',index=False)
    #print(df)
    list_a=[]
    list_b=[]
    list_skt=[]
    AKA_away_team = list_columnas[6].split()[0]  # 'NSH'
    AKA_home_team = list_columnas[7].split()[0]  # 'TBL'
    teams=[AKA_away_team,AKA_home_team]

    for indice, team_jugadas in enumerate(teams):
        #print('Team Jugadas:', team_jugadas)
        indice_otro_team=1-indice
        team_players=teams[indice_otro_team]
        #print('Team Players:',team_players)
        df_home=df[df['Team'] == team_jugadas]
        df_home_EV=df_home[df_home['Str']=='EV']
        skaters_edit=skaters[skaters['Team']==team_jugadas]
        for valor in skaters_edit['sweaterNumber']:
            # Filtrar el DataFrame usando el valor actual de 'sweaterNumber'
            id_skaters=skaters_edit[skaters_edit['sweaterNumber']==valor]
            number_id = id_skaters['playerId'].iloc[0]
            poss_id = id_skaters['position'].iloc[0]
            goal_id = id_skaters['goals'].iloc[0]
            assis_id = id_skaters['assists'].iloc[0]
            point_id = id_skaters['points'].iloc[0]
            pim_id = id_skaters['pim'].iloc[0]
            hits_id = id_skaters['hits'].iloc[0]
            shot_id = id_skaters['shots'].iloc[0]
            toi_id = id_skaters['toi'].iloc[0]
            #print('ID_SKATERS:',poss_id, goal_id,assis_id,point_id,pim_id,hits_id,shot_id,toi_id )
            list_skt.append({'id_skaters':number_id,
                             'position':poss_id,
                             'goals':goal_id,
                             'assists':assis_id,
                             'points':point_id,
                             'pim':pim_id,
                             'hits':hits_id,
                             'shot':shot_id,
                             'toi':toi_id})
            #df_home_EV[f'{team_jugadas} On Ice'] = df_home_EV[f'{team_jugadas} On Ice'].apply(convertir_a_lista)
            df_home_EV.loc[:, f'{team_jugadas} On Ice'] = df_home_EV[f'{team_jugadas} On Ice'].apply(convertir_a_lista)
            df_home_EV_filtrada = df_home_EV[df_home_EV[f'{team_jugadas} On Ice'].apply(lambda x: valor in x)]
            # Contar la cantidad de eventos de cada tipo en el DataFrame filtrado
            shot_count_cf = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'SHOT'].shape[0]
            miss_count_cf = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'MISS'].shape[0]
            block_count_cf = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'BLOCK'].shape[0]
            goal_count_cf = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'GOAL'].shape[0]
            
            # Calcular el total de eventos
            cf_player_cf = shot_count_cf + miss_count_cf + block_count_cf + goal_count_cf

            list_a.append({'team':team_jugadas,
                        'IdMatch':idMatch_fila,
                        'gameType': gametype,
                        'sweaterNumber':valor,
                        'id_skaters':number_id,
                        'shot_cf':shot_count_cf,
                        'miss_cf':miss_count_cf,
                        'block_cf':block_count_cf,
                        'goal_cf':goal_count_cf,
                        'CF':cf_player_cf})

        skaters_edit=skaters[skaters['Team']==team_players]
        for valor in skaters_edit['sweaterNumber']:
            #print(valor)
            # Filtrar el DataFrame usando el valor actual de 'sweaterNumber'
            id_skaters=skaters_edit[skaters_edit['sweaterNumber']==valor]
            number_id = id_skaters['playerId'].iloc[0]
            df_home_EV.loc[:, f'{team_players} On Ice'] = df_home_EV[f'{team_players} On Ice'].apply(convertir_a_lista)
            #df_home_EV[f'{team_players} On Ice'] = df_home_EV[f'{team_players} On Ice'].apply(convertir_a_lista)
            df_home_EV_filtrada = df_home_EV[df_home_EV[f'{team_players} On Ice'].apply(lambda x: valor in x)]
            # Contar la cantidad de eventos de cada tipo en el DataFrame filtrado
            shot_count_ca = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'SHOT'].shape[0]
            miss_count_ca = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'MISS'].shape[0]
            block_count_ca = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'BLOCK'].shape[0]
            goal_count_ca = df_home_EV_filtrada[df_home_EV_filtrada['Event'] == 'GOAL'].shape[0]
            
            # Calcular el total de eventos
            ca_player_ca = shot_count_ca + miss_count_ca + block_count_ca + goal_count_ca

            url_player=f'https://api-web.nhle.com/v1/player/{number_id}/landing'
            response=requests.get(url_player)
            #print(response)
            data_name=response.json()
            name=data_name['firstName']['default']
            apellido=data_name['lastName']['default']

            list_b.append({'team':team_players,
                        'IdMatch':idMatch_fila,
                        'gameType': gametype,
                        'sweaterNumber':valor,
                        'id_skaters':number_id,
                        'shot_ca':shot_count_ca,
                        'miss_ca':miss_count_ca,
                        'block_ca':block_count_ca,
                        'goal_ca':goal_count_ca,
                        'CA':ca_player_ca})


            #PRUEBA#
            
    #Con esto filtro el 5vs5:
            #df_filtrado = df.loc[(df[list_columnas[6]].apply(len) == 6) & (df[list_columnas[7]].apply(len) == 6)]
    #print(list_a)
    df_players_cf=pd.DataFrame(list_a)
    #print(df_players_cf)

    df_players_ca=pd.DataFrame(list_b)
    #print(df_players_ca)

    df_players=pd.DataFrame(list_skt)
    #print(df_players)
    merged_df = pd.merge(df_players_cf, df_players_ca, on=['IdMatch','gameType','team', 'sweaterNumber','id_skaters'], how='outer')
    #print(merged_df)
    otro_merged=pd.merge(merged_df,df_players,on=['id_skaters'])
    #print('Otro Merged:',otro_merged)
    final_list.append(otro_merged)
#print('final list:',final_list)


df_concat=pd.DataFrame()
for df in final_list:
    #print(df)
    #print(type(df))
    df_concat=pd.concat([df_concat,df], ignore_index=True)
#print(df_concat)

column_names = ['IdMatch','gameType','team','id_skaters','position','sweaterNumber','goals','assists','points','pim','hits','shot','toi','shot_cf', 'miss_cf', 'block_cf', 'goal_cf', 'CF', 'shot_ca', 'miss_ca', 'block_ca', 'goal_ca', 'CA']
df_concat = df_concat.reindex(columns=column_names)

# # Función para obtener nombre y apellido a partir del ID
# def obtener_nombre_apellido(number_id):
#     url_player = f'https://api-web.nhle.com/v1/player/{number_id}/landing'
#     try:
#         response = requests.get(url_player)
#         data_name = response.json()
#         # Obtener los valores del JSON, asumiendo que la estructura es correcta
#         name = data_name.get('firstName', {}).get('default', 'N/A')
#         last_name = data_name.get('lastName', {}).get('default', 'N/A')
#         return pd.Series([name, last_name])
#     except Exception as e:
#         print(f"Error al obtener datos para el ID {number_id}: {e}")
#         return pd.Series(['N/A', 'N/A'])  # Valores por defecto si hay error

# # Aplicar la función a cada fila del DataFrame y asignar a las nuevas columnas
# df_concat[['name', 'last_name']] = df_concat['IdMatch'].apply(obtener_nombre_apellido)

df_concat.to_csv("Data_csv/Test_Players_2023-2024.csv", index=False)




