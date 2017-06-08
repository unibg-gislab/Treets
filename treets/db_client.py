#! /urs/bin/python
# coding: utf8
from __future__ import print_function
import pymongo
from random import uniform


class DBClient(object):
    '''Docstring for DBClient'''

    def __init__(self):
        super(DBClient, self).__init__()
        self.mongo = pymongo.MongoClient()
        self.db = self.mongo.test
        self.db.tweets.ensure_index([('location', pymongo.GEOSPHERE)])
        self.check_text_index()

    def create_locations(self):
        print('creating locations for geo-indexing, this may take a while')
        for t in self.db.tweets.find():
            coords = t['geo']
            t['location'] = {'type': 'Point', 'coordinates': coords[::-1]}
            self.db.tweets.save(t)

    def check_text_index(self):
        try:
            self.db.tweets.create_index([('textMessage', 'text')])
        except:
            print('converting texts to unicode, this may take a while')
            for t in self.db.tweets.find():
                t['textMessage'] = unicode(t['textMessage'])
                self.db.tweets.save(t)
            self.db.tweets.create_index([('textMessage', 'text')])

    def get_tweets(self, limit=1000):
        '''
        Returns first <limit> tweets
        '''
        return self.db.tweets.find().limit(limit)

    def get_random_tweets(self, limit=1000):
        '''
        returns <limit> random tweets
        '''
        lenght = self.db.tweets.find().count()
        rand = int(uniform(0, 1)*lenght)
        return self.db.tweets.find().limit(limit).skip(rand)

    def get_tweets_near_point(self, coords, dist, limit=1000):
        '''
        returns <limit> tweets whithin <dist> meters from coords
        '''
        return self.db.tweets.find({
            'location': {
                '$nearSphere': {
                    '$geometry': {
                        'type': 'Point', 'coordinates': coords
                    }, '$maxDistance': dist
                }
            }
        }).limit(limit)

    def get_tweets_for_text(self, text, limit=1000):
        '''
        search for tweets containing <text> and returns results
        '''
        return self.db.tweets.find({'$text': {'$search': text}})

    def get_tweets_for_user(self, user):
        '''
        returns tweets posted by user
        '''
        return self.db.tweets.find({"userName": user})

    def get_traces(self, limit=100):
        '''
        Returns first <limit> lists of tweets from the same users
        '''
        users = self.db.tweets.distinct('userName')[:limit]
        cursors = []
        for user in users:
            cursors.append(self.get_tweets_for_user(user))
        return cursors

    def get_traces_near_point(self, coords, dist, limit=100):
        '''
        TODO docstring
        '''
        tweets = self.get_tweets_near_point(coords, dist, limit=1000)
        users = tweets.distinct('userName')[:limit]
        cursors = []
        for user in users:
            cursors.append(self.get_tweets_for_user(user))
        return cursors

    def get_traces_for_text(self, text, limit=100):
        '''
        TODO docstring
        '''
        tweets = self.get_tweets_for_text(text, limit=1000)
        users = tweets.distinct('userName')[:limit]
        cursors = []
        for user in users:
            cursors.append(self.get_tweets_for_user(user))
        return cursors




if __name__ == '__main__':
    pass
