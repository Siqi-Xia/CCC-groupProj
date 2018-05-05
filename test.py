import json
import re
import folium
from folium.plugins import HeatMap
import pycouchdb

###############################################################
# 'aurin_coords' is a list of coordinates that stores vehicle #
# crash locations in 2017                                     #
###############################################################

AURIN_FILE = 'aurin_file.json'

aurin_coords = []

with open(AURIN_FILE) as f:
    data = json.loads(f.read())
    for feature in data["features"]:
        # "\d+\/\d+\/2017"
        accident_date = feature["properties"]["ACCIDENT_DATE"]
        if re.match(r'\d+/\d+/2017', accident_date):
            coords = [feature["geometry"]["coordinates"][1],
                      feature["geometry"]["coordinates"][0]]
            print coords
            aurin_coords.append(coords)


#################################################################
# 'liquor_coords' is a list of coordinates that stores licenced #
# liquor stores' location                                       #
#################################################################


AURIN_LIQUOR = 'data_liquor_licence.json'

liquor_coords = []

with open(AURIN_LIQUOR) as f2:
    data = json.loads(f2.read())
    for feature in data['features']:
        coords = [feature['geometry']['coordinates'][1],
                  feature['geometry']['coordinates'][0]]
        liquor_coords.append(coords)


#################################################################
# 'tweet_coords' is a list of coordinates that stores locations #
# of alcohol related tweets                                     #
#################################################################


ALCOHOL_RELATED = ['alcohol', 'drink', 'cider', 'bbooze', 'beer', 'drunk',
                   'stoned', 'wasted', 'plastered', 'smashed', 'wrecked', 'high', 'beer',
                   'vodka', 'wine', 'alcoholic', 'champagne', 'hennessey', 'grey goose',
                   'truth serum', 'beverage', 'ale', 'liquor', 'liqueur', 'meaning of life',
                   'drinking', 'whiskey', 'spirits', 'malt', 'bar', 'bars', 'honkytonk',
                   'party', 'shitfaced', 'hangover', 'shit faced', 'tanked', 'sloshed',
                   'trashed', 'blackout', 'pissed']

server = pycouchdb.Server('http://admin:admin@localhost:5984')
db = server.database('db_twitters')
result = list(db.query('coordinates/id_str'))

tweet_coords = []
for tweet in result:
    data = tweet['value']
    for term in ALCOHOL_RELATED:
        tweet_msg = [word.lower() for word in data['text']]
        if term in tweet_msg:
            coords = [data['coordinates']['coordinates'][1],
                      data['coordinates']['coordinates'][0]]
            tweet_coords.append(coords)

"""
TWEET_FILE = 'data.json'

coords_list2 = []
with open(TWEET_FILE) as f3:
    f3.readline()
    for line in f3:
        try:
            data = json.loads(line[0:len(line) - 2])
            if data["coordinates"]["coordinates"]:
                for term in ALCOHOL_RELATED:
                    tweet_msg = [word.lower() for word in data['text']]
                    if term in tweet_msg:
                        print 'Tweet Text:', data['text']
                        print 'Term Found:', term
                        coords = [data["coordinates"]["coordinates"][1],
                                  data["coordinates"]["coordinates"][0]]
                                  # data["coordinates"]["coordinates"][lat, lgt]
                        coords_list2.append(coords)
                        print coords
        except TypeError:
            continue
        except ValueError:
            data = json.loads(line[0:len(line) - 1])
            if data["coordinates"]:
                coords = [data["coordinates"]["coordinates"][1],
                          data["coordinates"]["coordinates"][0]]
                coords_list2.append(coords)
                print coords
            break
"""

map_crash = folium.Map(location=[-37.814, 144.96332], zoom_start=5)
HeatMap(aurin_coords, radius=8).add_to(map_crash)
file_path1 = r'crash_heatmap.html'
map_crash.save(file_path1)

map_liquor = folium.Map(location=[-37.814, 144.96332], zoom_start=5)
HeatMap(liquor_coords, radius=8).add_to(map_liquor)
file_path2 = r'liquor_heatmap.html'
map_liquor.save(file_path2)

map_tweet = folium.Map(location=[-37.814, 144.96332], zoom_start=5)
HeatMap(tweet_coords).add_to(map_tweet)
file_path3 = r'tweet_heatmap.html'
map_liquor.save(file_path3)

