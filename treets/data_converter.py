import geojson
import pandas as pd


class DataConverter(object):
    """docstring for DataConverter"""

    def __init__(self):
        super(DataConverter, self).__init__()

    def tweet_to_feature(self, tweet):
        '''
        convert tweet to a geojson feature
        '''
        point = tweet['location']
        properties = tweet
        for key in ['geo', 'location', 'data']:
            del properties[key]
        return geojson.Feature(geometry=point, properties=properties)

    def tweets_to_feature_collection(self, tweets):
        '''
        convert list of tweets to a geojson feature collection
        '''
        features = [self.tweet_to_feature(tweet) for tweet in tweets]
        return geojson.FeatureCollection(features)

    def tweets_to_table(self, tweets):
        '''
        convert list of tweets to a pandas table
        '''
        return pd.DataFrame.from_records(tweets)
