  

#twitter time

import tweepy
from tweepy import Stream
from tweepy import StreamListener 
from tweepy import OAuthHandler
import os 
import json
import numpy as np
from datetime import *



consumer_key = "u8Kx69mcOFPHbd309uKDQfDOA"
consumer_secret = "gkrfQLzeXoU0oOxODIk0weowzJc8opUIzop5UlpaAEQLyyWmhy"
access_token = "381766751-mfUc9PGRIJ7ZuAFRoREuPWz6HaS7SkGQFyXlf2vd"
access_secret = "XXYUWEc63Dvp68mJKwibIUJ7wFlByHf0O4SK65WTzHO6J"
#consumer_key = "qaFn3UVPmprNsqlF25TtSszL5"
#consumer_secret = "r5cLVPV5ZrEWclssU7MWGjBZxtm9HKTT8Z0uQfK0po20cnDwKh"
#access_token = "989757353258975234-XCMOO4eR0XBQdJhYPvAHJ6AqRIkSSuj"
#access_secret = "bsmeX1gMVOWaf8xZ6hBuq0Se2qF8SY9tNFfuZcKQUbd4X"

TWEET_NUM=5000
#filename=datetime.now().strftime("%Y%m%d%H%M%S")+".json"
#print("output file name:",filename)
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

#search by country
places = api.geo_search(query="Australia", granularity="country")
#search by city
places = api.geo_search(query="Melbourne", granularity="city")


#print(places)

bb=places[0].bounding_box.coordinates[0]
bb=np.array(bb)
#use a rough bounding box (rectangle) instead of a rigid polygon
bounding_box=[np.min(bb[:,0]),np.min(bb[:,1]),np.max(bb[:,0]),np.max(bb[:,1])]
print("bounding box is",bounding_box)
place_id = places[0].id




print("============================")

if os.path.exists('data'):
    print("folder exists")
else:
    os.mkdir('data')
    print ("new data folder.")

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
cnt=0
class MyListener(StreamListener):
    def __init__(self, api=None):
       super(self.__class__, self).__init__()
       self.num_tweets = 0
       self.firstdata=1


    def on_data(self, data):
        try:
            not_duplicated = True
            #add database operation here....
            #idmap = list(db.query("idmap/id"))
            #lj=json.loads(data)
            #for item in idmap:
             #   if lj["id"] == item["key"]:
              #      not_duplicated = False
            #print(idmap)
            #print(type(lj))
            #print(lj["id"])    
            if not_duplicated :
                db.save(lj)
                self.num_tweets+=1
                filename="data/"+datetime.now().strftime("%Y%m%d%H%M%S")+".json"
                print("output file name:",filename)
                print("sampled %d data"%self.num_tweets)
                with open(filename,"a",encoding="utf-8") as f2:
                    #if self.firstdata!=1:
                    #  f2.write(",\n")
                    lj=json.loads(data)
                    #self.firstdata=0
                    x=json.dumps(lj)
                    f2.write(x)
            else:
                print("duplicated twit")


        except BaseException as e:
            print("Error on_data: %s" % str(e))

        if self.num_tweets>=TWEET_NUM:
            return False
            
        return True
 
    def on_error(self, status):
        print(status)

        return True

    #https://github.com/tweepy/tweepy/issues/935
    #returning False in on_error disconnects the stream
    #prevent the exponentially increased time of rate limiting  
    def test_rate_limit(api, wait=True, buffer=.1):
            """
            Tests whether the rate limit of the last request has been reached.
            :param api: The `tweepy` api instance.
            :param wait: A flag indicating whether to wait for the rate limit reset
                     if the rate limit has been reached.
            :param buffer: A buffer time in seconds that is added on to the waiting
                       time as an extra safety margin.
            :return: True if it is ok to proceed with the next request. False otherwise.
            """
            #Get the number of remaining requests
            remaining = int(api.last_response.getheader('x-rate-limit-remaining'))
            #Check if we have reached the limit
            if remaining == 0:
                limit = int(api.last_response.getheader('x-rate-limit-limit'))
                reset = int(api.last_response.getheader('x-rate-limit-reset'))
                #Parse the UTC time
                reset = datetime.fromtimestamp(reset)
                #Let the user know we have reached the rate limit
                print("0 of {} requests remaining until {}.".format(limit, reset))

            if wait:
                #Determine the delay and sleep
                delay = (reset - datetime.now()).total_seconds() + buffer
                print("Sleeping for {}s...".format(delay))
                sleep(delay)
                #We have waited for the rate limit reset. OK to proceed.
                return True
            else:
                #We have reached the rate limit. The user needs to handle the rate limit manually.
                return False 

            #We have not reached the rate limit
            return True

twitter_stream = Stream(auth, MyListener())

print("stream connected!")

#with open(filename,"w",encoding="utf-8") as f2:
   # f2.write("{\"total_rows\":%d,\"offset\":0,\"rows\":[\n"%TWEET_NUM)

#its said that filter can search data in 7 days, while api.search can only search data in a much shorter time
twitter_stream.filter(locations=bounding_box)  #track=['sleep']   #add hashtag

#with open(filename,"a",encoding="utf-8") as f2:
    #f2.write("\n]}\n")
# tweets = api.search(q="place:%s" % place_id,count=1000)
# for tweet in tweets:
#     print( tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place")




print("sampled finish!!!!!!!")
