from __future__ import print_function
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

    def save_geojson(self, data, fname):
        '''
        Export geojson to file
        '''
        with open(fname, 'wb') as f:
            geojson.dump(data, f, sort_keys=True, indent=4)

    def tweets_to_table(self, tweets):
        '''
        convert list of tweets to a pandas table
        '''
        return pd.DataFrame.from_records(tweets)

    def save_dataframe(self, df, fname):
        '''
        Export dataframe to file
        '''
        df.to_csv(fname, index=False)
