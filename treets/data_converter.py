from __future__ import print_function
from pandas import DataFrame
import geojson
import re


class DataConverter(object):
    """docstring for DataConverter"""

    def __init__(self):
        super(DataConverter, self).__init__()
        self.url_regex = re.compile(r'''((?:mailto:|ftp://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')

    def encode_string_with_links(self, unencoded_string):
        return self.url_regex.sub(r'<a target="_blank" href="\1">\1</a>', unencoded_string)

    def tweet_to_feature(self, tweet):
        '''
        convert tweet to a geojson feature
        '''
        point = tweet['location']
        properties = tweet
        for key in ['geo', 'location', 'data']:
            del properties[key]
        properties['textMessage'] = self.encode_string_with_links(properties['textMessage'])
        #print(properties['textMessage'])
        return geojson.Feature(geometry=point, properties=properties)

    def tweets_to_feature_collection(self, tweets):
        '''
        convert list of tweets to a geojson feature collection
        '''
        features = [self.tweet_to_feature(tweet) for tweet in tweets]
        tweets.rewind()
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
        return DataFrame.from_records(tweets)

    def save_dataframe(self, df, fname):
        '''
        Export dataframe to file
        '''
        df.to_csv(fname, index=False)
