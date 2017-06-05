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

    def tweet_to_row(self, tweet):
        '''
        convert tweet to a csv row
        '''
        pass

    def tweets_to_table(self, tweets):
        '''
        convert list of tweets to a pandas table
        '''
        #rows = [self.tweet_to_row(tweet) for tweet in tweets]
        pass
