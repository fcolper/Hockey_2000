import pandas as pd
import requests

archivo='Data_csv/CorsiMatches_2022-2023.csv'
archivo_base=pd.read_csv(archivo, sep=',') 
list_link=list(archivo_base['gameId'])

list_general=[]

for link in list_link:
    new_url=f'https://api-web.nhle.com/v1/gamecenter/{link}/landing'
    response=requests.get(new_url)
    data=response.json()
    print(new_url)
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

    diccionario_TEAM={
    'gameId':link,
    'First Goal Home':first_goal_home,
    'First Goal Away':first_goal_away,
    'SOG Home':sog_home,
    'SOG Away':sog_away,
    'Faceoff Home':face_home,
    'Faceoff Away':face_away,
    'Pim Home':pim_home,
    'Pim Away':pim_away
    }

    list_general.append(diccionario_TEAM)

df=pd.DataFrame(list_general)

guardar=pd.merge(archivo_base, df, on='gameId', how='outer')

guardar.to_csv(f'Data_csv/TeamsMatches_2022-2023.csv', index=False)


'''
url=f'https://api-web.nhle.com/v1/gamecenter/2023020204/landing'
response=requests.get(url)
print(response)
data=response.json()
print(int(data['summary']['scoring'][0]['goals'][0]['homeScore']))


print(data['summary']['teamGameStats'][1]['awayValue'])
sog_home=int(data['summary']['teamGameStats'][0]['homeValue'])
sog_away=int(data['summary']['teamGameStats'][0]['awayValue'])
face_home=float(data['summary']['teamGameStats'][1]['homeValue'])
face_away=float(data['summary']['teamGameStats'][1]['awayValue'])
pim_home=int(data['summary']['teamGameStats'][4]['homeValue'])
pim_away=int(data['summary']['teamGameStats'][4]['awayValue'])
hits_home=int(data['summary']['teamGameStats'][5]['homeValue'])
hits_away=int(data['summary']['teamGameStats'][5]['awayValue'])
blockedShots_home=int(data['summary']['teamGameStats'][6]['homeValue'])
blockedShots_away=int(data['summary']['teamGameStats'][6]['awayValue'])
giveaways_home=int(data['summary']['teamGameStats'][7]['homeValue'])
giveaways_away=int(data['summary']['teamGameStats'][7]['awayValue'])
takeaways_home=int(data['summary']['teamGameStats'][8]['homeValue'])
takeaways_away=int(data['summary']['teamGameStats'][8]['awayValue'])
print(face_home,face_away,sog_home,sog_away,pim_home,pim_away,hits_home,hits_away,blockedShots_home,blockedShots_away,giveaways_home,giveaways_away,takeaways_home,takeaways_away)

'''














