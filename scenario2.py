import pandas as pd
import json
import folium
import pycouchdb
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

sid = SentimentIntensityAnalyzer()
server = pycouchdb.Server('http://admin:admin@localhost:5984')
db = server.database('db_twitters')
result = list(db.query('coordinates/id_str'))

sid = SentimentIntensityAnalyzer()

tweet_coords = []
for tweet in result:
    data = tweet['value']
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


SMALL_BUSINESS = 'number of business.csv'
OCCUPATION_NUMBER = 'occupati numbers.csv'

df = pd.read_csv(SMALL_BUSINESS)
df[' sml_bus_emply_cnt'] = df[' bus_1_4_emply_cnt'] + df[' bus_5_19_emply_cnt']
df[' sa2_name16'] = df[' sa2_name16'].str.upper()
df1 = pd.read_csv(OCCUPATION_NUMBER)
df1[' sa2_name16'] = df1[' sa2_name16'].str.upper()
merged_df1 = pd.merge(df, df1)
merged_df1['avg_bus_num'] = merged_df1[' sml_bus_emply_cnt']/merged_df1[' p_tot_tot']

df2 = pd.read_csv(OCCUPATION_NUMBER)
df2[' sa2_name16'] = df2[' sa2_name16'].str.upper()
df2['avg_happiness'] = None
for index in range(len(df2)):
    try:
        suburb = suburbs[feature['properties'][df2.loc[index, ' sa2_name16']]]
        df2.loc[index, 'avg_happiness'] = suburb['count_pos']/suburb['count']
    except KeyError:
        df2.loc[index, 'avg_happiness'] = 0
merged_df = pd.merge(merged_df1, df2)
merged_df['result'] = merged_df['avg_bus_num'] * merged_df['avg_happiness']

m = folium.Map(
    location=[-37.814, 144.96332],
    zoom_start=5,
    tiles='cartodbpositron'
)

m.choropleth(
    geo_data=VIC_BOUNDARY,
    name='choropleth',
    data=merged_df,
    columns=[' sa2_name16', 'avg_happiness'],
    key_on='feature.properties.vic_loca_2',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2
)

folium.LayerControl().add_to(m)
m.save(r'choropleth.html')














