# import pandas as pd
# import time
# from geopy.geocoders import Nominatim

# # Cargar los datos
# df = pd.read_csv('Data_csv/Players_20002024.csv')

# # Tomamos solo las primeras 5 filas como ejemplo
# df_1= df.head(50).copy() 
# df_1 = df[df['id'] == 8482149].copy()

# country_dict = {
#     'CAN': 'Canada',
#     'USA': 'United States',
#     'SWE': 'Sweden',
#     'RUS': 'Russia',
#     'FIN': 'Finland',
#     'CZE': 'Czech Republic',
#     'SVK': 'Slovakia',
#     'SUI': 'Switzerland',
#     'GER': 'Germany',
#     'LAT': 'Latvia',
#     'BLR': 'Belarus',
#     'DEN': 'Denmark',
#     'UKR': 'Ukraine',
#     'NOR': 'Norway',
#     'AUT': 'Austria',
#     'GBR': 'United Kingdom',
#     'KAZ': 'Kazakhstan',
#     'FRA': 'France',
#     'POL': 'Poland',
#     'LTU': 'Lithuania',
#     '{}': None,  # Reemplaza si sabes a qué país corresponde o trata los datos faltantes
#     'BEL': 'Belgium',
#     'ITA': 'Italy',
#     'SLO': 'Slovenia',
#     'JPN': 'Japan',
#     'CRO': 'Croatia',
#     'BAH': 'Bahamas',
#     'KOR': 'South Korea',
#     'NGR': 'Nigeria',
#     'BRA': 'Brazil',
#     'RSA': 'South Africa',
#     'BRU': 'Brunei',
#     'IDN': 'Indonesia',
#     'EST': 'Estonia',
#     'TAN': 'Tanzania',
#     'NED': 'Netherlands',
#     'AUS': 'Australia',
#     'UZB': 'Uzbekistan',
#     'BUL': 'Bulgaria'
# }

# from opencage.geocoder import OpenCageGeocode
# import pandas as pd
# import time

# # Reemplaza con tu clave API de OpenCage
# key = 'd699b07e72bf4cfebf9ff376a57ee69c'
# geocoder = OpenCageGeocode(key)

# # Función para obtener latitud y longitud con OpenCage, considerando tanto ciudad como país
# def get_lat_lon_opencage(row):
#     country_full = country_dict.get(row['country'], row['country'])  # Convertir abreviación a nombre completo
#     query = f"{row['city']}, {country_full}"  # Asegurarte de incluir tanto ciudad como país completo
#     results = geocoder.geocode(query)
#     if results and len(results):
#         return pd.Series([results[0]['geometry']['lat'], results[0]['geometry']['lng']])
#     else:
#         return pd.Series([None, None])

# # Aplicar la función a cada fila
# df_1[['latitude', 'longitude']] = df_1.apply(get_lat_lon_opencage, axis=1)

# # Agregar un pequeño delay entre consultas para evitar sobrecarga en el servicio
# time.sleep(1)

# # Mostrar el DataFrame con latitud y longitud
# df_1.to_csv('Data_csv/Players_20002024_latlong_5.csv')

# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns 

# csv_2018='Data_csv/Players_20002024_.csv'
# csv_2017='Data_csv/Players_20002024_latlong_5.csv'
# csv_2016='Data_csv/Players_20002024.csv'

# df_2018=pd.read_csv(csv_2018)
# df_2017=pd.read_csv(csv_2017)
# df_2016=pd.read_csv(csv_2016)

# df_2017=df_2017.drop(columns=['Unnamed: 0'])


# df_2018=df_2018.drop_duplicates(subset=['id'])

# df=pd.concat([df_2018,df_2017], ignore_index=True)

# df=df.drop_duplicates(subset=['id'])

# df.sort_values(by=['id'], inplace=True)
# df.to_csv(f'Data_csv/Players_20002024_1.csv', index=False)

# import pandas as pd
# import folium

# # Paso 3: Cargar el DataFrame (a partir de tu CSV o DataFrame existente)
# # Si el DataFrame ya está cargado, puedes saltarte esta parte
# df = pd.read_csv('Data_csv/Players_20002024.csv')

# # Paso 4: Crear un mapa centrado en el mundo
# # El mapa puede estar centrado en unas coordenadas iniciales (por ejemplo, 0,0 para un mapa global)
# m = folium.Map(location=[0, 0], zoom_start=2)

# # Paso 5: Iterar sobre cada fila del DataFrame y agregar los puntos al mapa
# for index, row in df.iterrows():
#     folium.Marker(
#         location=[row['latitude'], row['longitude']],
#         popup=f"{row['firstName']} {row['lastName']} - {row['city']}, {row['country']}",
#         icon=folium.Icon(color="blue", icon="info-sign")
#     ).add_to(m)

# # Paso 6: Guardar el mapa en un archivo HTML o mostrarlo directamente
# m.save('jugadores_mapa.html')

import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Paso 1: Cargar el DataFrame (a partir de tu CSV o DataFrame existente)
df = pd.read_csv('Data_csv/Players_20002024.csv')

# Paso 2: Crear un mapa centrado en el mundo
m = folium.Map(location=[0, 0], zoom_start=2)

# Paso 3: Crear un diccionario de capas por país
country_groups = df.groupby('country')

# Paso 4: Iterar sobre cada país y agregar una capa por país
for country, group in country_groups:
    # Crear un FeatureGroup para cada país
    feature_group = folium.FeatureGroup(name=country)

    # Agregar un MarkerCluster para mejorar el rendimiento si hay muchos puntos
    marker_cluster = MarkerCluster().add_to(feature_group)

    # Iterar sobre cada jugador del país actual
    for index, row in group.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['firstName']} {row['lastName']} - {row['city']}, {row['country']}",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(marker_cluster)

    # Añadir la capa del país al mapa
    feature_group.add_to(m)

# Paso 5: Añadir control de capas para habilitar/deshabilitar países
folium.LayerControl().add_to(m)

# Paso 6: Guardar el mapa en un archivo HTML
m.save('jugadores_mapa_filtrado_2.html')

