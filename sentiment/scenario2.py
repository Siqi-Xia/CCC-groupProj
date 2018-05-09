import pandas as pd
from pandas.io.json import json_normalize
import json
import folium
import couchdbProcesser as query
from shapely.geometry import MultiPoint
from shapely.geometry import Point
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

map_boundary = query.get_data('db_aurin', 'geoserver-GetFeature')
suburbs = {}

for feature in map_boundary['features']:
    coordinates = feature['geometry']['coordinates'][0][0]
    #print feature['properties']['vic_loca_2']
    coordinate_tuple = [(coordinate[0], coordinate[1]) for coordinate in coordinates]
    #print len(coordinate_tuple)
    poly = MultiPoint(coordinate_tuple).convex_hull
    suburbs[feature['properties']['vic_loca_2']] = {'poly': poly, 'count': 0, 'count_pos': 0}

sid = SentimentIntensityAnalyzer()
result = query.query_view('db_twitters','coordinates')

print 'Boundary map constructed!'
print len(suburbs)

sid = SentimentIntensityAnalyzer()

i = 0
j = 0
for tweet in result:
    #print ('count:', i)
    i += 1
    coordinates = tweet['value']['coordinates']['coordinates']
    point = Point(coordinates[0], coordinates[1])
    loop_flag = True
    for suburb in suburbs.keys():
        for key, value in suburbs[suburb].items():
	    if key == 'poly':
		poly = value
                if poly.contains(point):
                    suburbs[suburb]['count'] += 1
                    scores = sid.polarity_scores(tweet['value']['text'])
                    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
                    if sorted_scores[0][0] != 'neg':
                        suburbs[suburb]['count_pos'] += 1
		    loop_flag = False
                    break
        if loop_flag == False:
	    break
#print suburbs        

SMALL_BUSINESS = query.get_data("db_aurin","Data_by_Region_Economy_Industry_2011-2016")
OCCUPATION_NUMBER = query.get_data("db_aurin","status_in_Employment_2016")

#print type(SMALL_BUSINESS)
temp_list = [feature['properties'] for feature in SMALL_BUSINESS['features']]
df = pd.DataFrame(temp_list)
#print df.columns.values.tolist()

df['sml_bus_emply_cnt'] = df['bus_1_4_emply_cnt'] + df['bus_5_19_emply_cnt']
df['sa2_name16'] = df['sa2_name16'].str.upper()
temp_list1 = [feature['properties'] for feature in OCCUPATION_NUMBER['features']]
df1 = pd.DataFrame(temp_list1)
df1['sa2_name16'] = df1['sa2_name16'].str.upper()
merged_df1 = pd.merge(df, df1)
merged_df1['avg_bus_num'] = merged_df1['sml_bus_emply_cnt']/merged_df1['p_tot_tot']

df2 = pd.DataFrame(temp_list1)
df2['sa2_name16'] = df2['sa2_name16'].str.upper()
df2['avg_happiness'] = None
for index in range(len(df2)):
    try:
        suburb = suburbs[feature['properties'][df2.loc[index, 'sa2_name16']]]
        df2.loc[index, 'avg_happiness'] = suburb['count_pos']/suburb['count']
    except KeyError:
        df2.loc[index, 'avg_happiness'] = 0

#print merged_df


m = folium.Map(
    location=[-37.814, 144.96332],
    zoom_start=10,
    tiles='cartodbpositron'
)

m.choropleth(
    geo_data=map_boundary,
    name='choropleth',

    data=merged_df1,
    columns=['sa2_name16', 'avg_bus_num'],
    key_on='feature.properties.vic_loca_2',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2
)

file_path = r'/doc/analysis/sentiment/html/choropleth.html'
folium.LayerControl().add_to(m)
m.save(file_path)


m1 = folium.Map(
    location=[-37.814, 144.96332],
    zoom_start=10,
    tiles='cartodbpositron'
)

m1.choropleth(
    geo_data=map_boundary,
    name='choropleth1',

    data=df2,
    columns=['sa2_name16', 'avg_happiness'],
    key_on='feature.properties.vic_loca_2',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2
)

file_path1 = r'/doc/analysis/sentiment/html/choropleth1.html'
folium.LayerControl().add_to(m1)
m1.save(file_path1)












