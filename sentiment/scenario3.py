import pandas as pd
import json
import folium
from shapely.geometry import MultiPoint
from shapely.geometry import Point
import nltk
import couchdbProcesser as query
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
    suburbs[feature['properties']['vic_loca_2']] = {'poly': poly, 'late_sleep_count': 0, 'all_day_count': 0}

sid = SentimentIntensityAnalyzer()
late_sleep_data = query.query_view('db_twitters','stayuplateinworkday')
all_day_data = query.query_view('db_twitters', 'twitterinworkday')

sid = SentimentIntensityAnalyzer()

print len(late_sleep_data)
print len(all_day_data)

i = 0
for tweet in late_sleep_data:
    #print ('count:', i)
    i += 1
    coordinates = tweet['value']['coordinates']
    point = Point(coordinates[0], coordinates[1])
    loop_flag = True
    for suburb in suburbs.keys():
        for key, value in suburbs[suburb].items():
            if key == 'poly':
                poly = value
                if poly.contains(point):
                    suburbs[suburb]['late_sleep_count'] += 1
                    loop_flag = False
                    break
        if loop_flag == False:
            break

j = 0
for tweet in all_day_data[:2000]:
    print ('count:', j)
    j += 1
    coordinates = tweet['value']['coordinates']
    point = Point(coordinates[0], coordinates[1])
    loop_flag = True
    for suburb in suburbs.keys():
        for key, value in suburbs[suburb].items():
            if key == 'poly':
                poly = value
                if poly.contains(point):
                    suburbs[suburb]['all_day_count'] += 1
                    loop_flag = False
                    break
        if loop_flag == False:
            break 

ECONOMIC_INDEX = query.get_data('db_aurin','2016_The_Index_of_Economic_Resources')
temp_list = [feature['properties'] for feature in ECONOMIC_INDEX['features']]
df = pd.DataFrame(temp_list)
df['sa2_name16'] = df['sa2_name16'].str.upper()

df = df.sort_values(by=['state_rank'])
df['sleep_late_tweet_%'] = None

for index in range(len(df)):
    try:
        suburb = suburbs[df.loc[index, 'sa2_name16']]
        df.loc[index, 'sleep_late_tweet_%'] = suburb['late_sleep_count'] / suburb['all_day_count']
    except KeyError:
        continue
    except ZeroDivisionError:
	continue

df['available_rank'] = None
rank = 1
for index in range(len(df)):
    if df.loc[index, 'sleep_late_tweet_%'] != None:
        df.loc[index, 'available_rank'] = rank
        rank += 1

df = df.sort_values(by=['sleep_late_tweet_%'], ascending=False)
for index in range(len(df)):
    df.loc[index, 'sleep_rank'] = index

df = df.sort_values(by=['available_rank'])

json_file = {"type":"FeatureCollection","totalFeatures":0,"features": []}

for index in range(len(df)):
    feature_dict = {
		    "Type":"Feature", 
 		    "vic_loca_2":df.loc[index, 'sa2_name16'],
		    "late_slp_rank":df.loc[index, 'sleep_rank'],
		    "eco_index_rank":df.loc[index, 'available_rank']
   		    }
    json_file['features'].append(feature_dict)

query.save_data('db_test', json_file)












