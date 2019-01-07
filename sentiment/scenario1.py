import json
import re
import folium
from folium.plugins import HeatMap
import couchdbProcesser as query
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

###############################################################
# 'aurin_coords' is a list of coordinates that stores vehicle #
# crash locations in 2017                                     #
###############################################################

AURIN_FILE = query.get_data('db_aurin', 'crashes_last_five_years_2017')

aurin_coords = []

data = AURIN_FILE['features']
for feature in data:
    # "\d+\/\d+\/2017"
    accident_date = feature["properties"]["ACCIDENT_DATE"]
    if re.match(r'\d+/\d+/2017', accident_date):
        coords = [feature["geometry"]["coordinates"][1],
                  feature["geometry"]["coordinates"][0]]
        aurin_coords.append(coords)


#################################################################
# 'liquor_coords' is a list of coordinates that stores licenced #
# liquor stores' location                                       #
#################################################################


AURIN_LIQUOR = query.get_data('db_aurin', 'Liquor_Licences_Gaming_Venues_2016')

liquor_coords = []

data = AURIN_LIQUOR['features']
for feature in data:
    coords = [feature['geometry']['coordinates'][1],
              feature['geometry']['coordinates'][0]]
    liquor_coords.append(coords)


#################################################################
# 'tweet_coords' is a list of coordinates that stores locations #
# of alcohol related tweets                                     #
#################################################################


result = query.query_view('db_twitters','alcohol_related')
sid = SentimentIntensityAnalyzer()

tweet_coords = []
for tweet in result:
    data = tweet['value']
    scores = sid.polarity_scores(data['text'])
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if sorted_scores[0][0] != 'neg':
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

map_crash = folium.Map(location=[-37.814, 144.96332], zoom_start=8)
HeatMap(aurin_coords, radius=8).add_to(map_crash)
file_path1 = r'/doc/analysis/sentiment/html/crash_heatmap.html'
map_crash.save(file_path1)

map_liquor = folium.Map(location=[-37.814, 144.96332], zoom_start=8)
HeatMap(liquor_coords, radius=8).add_to(map_liquor)
file_path2 = r'/doc/analysis/sentiment/html/liquor_heatmap.html'
map_liquor.save(file_path2)

map_tweet = folium.Map(location=[-37.814, 144.96332], zoom_start=8)
HeatMap(tweet_coords).add_to(map_tweet)
file_path3 = r'/doc/analysis/sentiment/html/tweet_heatmap.html'
map_liquor.save(file_path3)

