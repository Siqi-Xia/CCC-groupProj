import pandas as pd
import json
import folium
from shapely.geometry import MultiPoint
from shapely.geometry import Point
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


VIC_BOUNDARY = 'geoserver-GetFeature.json'
suburbs = {}

with open(VIC_BOUNDARY) as f:
    map_boundary = json.loads(f.read())
    for feature in map_boundary['features']:
        coordinates = feature['geometry']['coordinates'][0][0]
        #print feature['properties']['vic_loca_2']
        coordinate_tuple = [(coordinate[0], coordinate[1]) for coordinate in coordinates]
        #print len(coordinate_tuple)
        poly = MultiPoint(coordinate_tuple).convex_hull
        suburbs[feature['properties']['vic_loca_2']] = {'poly': poly, 'count': 0, 'count_pos': 0}

TWITTER_FILE = 'data.json'
sid = SentimentIntensityAnalyzer()

i = 0
coords_list2 = []
with open(TWITTER_FILE) as f:
    f.readline()
    for line in f:
        try:
            data = json.loads(line[0:len(line) - 2])
            if data["coordinates"]["coordinates"]:
                point = Point(data["coordinates"]["coordinates"][1],
                              data["coordinates"]["coordinates"][0])
                        # data["coordinates"]["coordinates"][lat, lgt]
                for suburb in suburbs.keys():
                    for dict in suburbs[suburb].items():
                        poly = dict[1][1]
                        if poly.contains(point):
                            suburbs[suburb]['count'] += 1
                            scores = sid.polarity_scores(data['text'])
                            sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
                            if sorted_scores[0][0] != 'neg':
                                suburbs[suburb]['count_pos'] += 1
                                print ++i
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

ECONOMICS_INDEX = 'index of ecnomic resources.csv'

df = pd.read_csv(ECONOMICS_INDEX)
df[' sa2_name16'] = df[' sa2_name16'].str.upper()
for index in range(len(df)):
    try:
        suburb = suburbs[feature['properties'][df.loc[index, ' sa2_name16']]]
        df.loc[index, 'tweet_count'] = suburb['count']
    except KeyError:
        df.loc[index, 'tweet_count'] = 0
df['tweet_pp'] = df['tweet_count']/df['usual_res_pop']

print df















