#! /urs/bin/python
# coding: utf8
from __future__ import print_function
from pandas import DataFrame
import geojson
import re
import sha


class DataConverter(object):
    """docstring for DataConverter"""

    def __init__(self):
        super(DataConverter, self).__init__()
        self.url_regex = re.compile(
            r'''((?:mailto:|ftp://|http://|https://)[^ <>'"{}|\\^`[\]]*)''')

    def encode_string_with_links(self, unencoded_string):
        return self.url_regex.sub(r'<a target="_blank" href="\1">\1</a>', unencoded_string)

    def tweet_to_feature(self, tweet):
        '''
        converts tweet to a geojson feature
        '''
        point = tweet['location']
        properties = tweet
        properties['_id'] = str(properties['_id'])
        for key in ['geo', 'location', 'data']:
            del properties[key]
        properties['textMessage'] = self.encode_string_with_links(properties[
                                                                  'textMessage'])
        properties['color'] = '#' + sha.sha(tweet['userName']).hexdigest()[:6]
        return geojson.Feature(geometry=point, properties=properties)

    def tweets_to_feature_collection(self, tweets):
        '''
        converts list of tweets to a geojson feature collection
        '''
        features = [self.tweet_to_feature(tweet) for tweet in tweets]
        tweets.rewind()
        return geojson.FeatureCollection(features)

    def trace_to_feature(self, trace, tweet_features):
        '''
        Converts a list of tweets to a geojson linestring, assuming all tweets
        are from the same user
        '''
        points = []
        properties = {}
        for tweet in trace:
            points.append(tweet['location']['coordinates'])
            tweet_features.append(self.tweet_to_feature(tweet))
        trace.rewind()
        line_String = geojson.LineString(points)
        properties['count'] = trace.count()
        properties['color'] = '#' + sha.sha(trace[0]['userName']).hexdigest()[:6]
        # TODO add starding  and ending dates as properties
        properties['userName'] = trace[0]['userName']
        return geojson.Feature(geometry=line_String, properties=properties)

    def traces_to_feature_collection(self, traces):
        '''
        converts list of lists of tweets to a geojson feature collection
        '''
        tweet_features = []
        traces_features = [self.trace_to_feature(t, tweet_features) for t in traces]

        return geojson.FeatureCollection(traces_features), geojson.FeatureCollection(tweet_features)

    def save_geojson(self, data, fname):
        '''
        Exports geojson to file
        '''
        with open(fname, 'wb') as f:
            geojson.dump(data, f, sort_keys=True, indent=4)

    def tweets_to_table(self, tweets):
        '''
        converts list of tweets to a pandas table
        '''
        table = []
        for tweet in tweets:
            t = {}
            t['userName'] = tweet['userName']
            t['stringDate'] = tweet['stringDate']
            t['stringTime'] = tweet['stringTime']
            t['Latitude'] = tweet['geo'][0]
            t['Longitude'] = tweet['geo'][1]
            t['textMessage'] = tweet['textMessage']
            t['url'] = 'http://twitter.com/' + tweet['userName'] + '/status/' +  str(tweet['_id'])
            table.append(t)
        return DataFrame.from_records(table)

    def save_dataframe(self, df, fname):
        '''
        Exports dataframe to file
        '''
        df.to_csv(fname, index=False)
