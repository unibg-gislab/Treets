#! /urs/bin/python
# coding: utf8
from __future__ import print_function
import pymongo
from random import uniform

TWEETS_LIMIT = 0
TRACES_LIMIT = 0

class DBClient(object):
    '''Docstring for DBClient'''

    def __init__(self):
        super(DBClient, self).__init__()
        self.mongo = pymongo.MongoClient()
        self.db = self.mongo.treets
        self.db.tweets.create_index('userName')
        self.db.users.create_index([('userName', 'text')])
        self.db.tweets.create_index([('textMessage', 'text')])
        self.db.tweets.ensure_index([('location', pymongo.GEOSPHERE)])
        #self.users = self.tweets.distinct('userName')[:limit]

    def setup_db(self):
        self.create_locations()
        self.check_text_index()
        self.create_users_collection()
        self.remove_users_and_tweets(100)

    def remove_users_and_tweets(self, threshold_max, threshold_min=1):
        found = self.db.users.find( { '$where': 'this.tweetsIds.length >' + str(threshold_max) })
        for u in found:
            self.db.tweets.remove({'_id': {'$in': u['tweetsIds']}})
            self.db.users.remove( u )

    def create_users_collection(self):
        self.db.users.remove()
        users = self.db.tweets.distinct('userName')
        users_coll = []
        for u in users:
            user = {}
            user['userName'] = u
            user['tweetsIds'] = self.db.tweets.find({'userName': u}).distinct('_id')
            users_coll.append(user)
        self.db.users.insert(users_coll)

    def create_locations(self):
        print('creating locations for geo-indexing, this may take a while')
        for t in self.db.tweets.find():
            coords = t['geo']
            t['location'] = {'type': 'Point', 'coordinates': coords[::-1]}
            self.db.tweets.save(t)
        self.db.tweets.ensure_index([('location', pymongo.GEOSPHERE)])

    def check_text_index(self):
        try:
            self.db.tweets.create_index([('textMessage', 'text')])
        except:
            print('converting texts to unicode, this may take a while')
            for t in self.db.tweets.find():
                t['textMessage'] = unicode(t['textMessage'])
                self.db.tweets.save(t)
            self.db.tweets.create_index([('textMessage', 'text')])

    def get_tweets(self, limit=TWEETS_LIMIT):
        '''
        Returns first <limit> tweets
        '''
        return self.db.tweets.find().sort([('_id', -1)]).limit(limit)

    def get_random_tweets(self, limit=TWEETS_LIMIT):
        '''
        returns <limit> random tweets
        '''
        lenght = self.db.tweets.find().count()
        rand = int(uniform(0, 1)*lenght)
        return self.db.tweets.find().limit(limit).skip(rand)

    def get_tweets_near_point(self, coords, dist, limit=TWEETS_LIMIT):
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
        }).sort([('_id', -1)])

    def get_tweets_for_text(self, text, limit=TWEETS_LIMIT):
        '''
        search for tweets containing <text> and returns results
        '''
        return self.db.tweets.find({'$text': {'$search': text}}).sort([('_id', -1)]).limit(limit)

    def get_tweets_for_user(self, user, limit=TWEETS_LIMIT):
        '''
        returns tweets posted by user
        '''
        return self.db.tweets.find({'_id': {'$in': user['tweetsIds']}})
        #return self.db.tweets.find({'userName': user}).sort([('_id', -1)]).limit(limit)

    def get_tweets_for_user_str(self, username, limit=TWEETS_LIMIT):
        user = self.db.users.find_one({'$text': {'$search': username}})
        return [self.get_tweets_for_user(user)]

    def get_traces(self, limit=TRACES_LIMIT):
        '''
        Returns first <limit> lists of tweets from the same users
        '''
        users = self.db.users.find().limit(limit)
        return [self.get_tweets_for_user(user) for user in users]

    def get_traces_near_point(self, coords, dist, limit=TRACES_LIMIT):
        '''
        TODO docstring
        '''
        users = self.get_tweets_near_point(coords, dist).distinct('userName')
        users_objs = self.db.users.find({'userName': {'$in': users}}).limit(limit)
        return [self.get_tweets_for_user(user) for user in users_objs]

    def get_traces_for_text(self, text, limit=TRACES_LIMIT):
        '''
        TODO docstring
        '''
        users = self.get_tweets_for_text(text, limit=limit).distinct('userName')
        users_objs = self.db.users.find({'userName': {'$in': users}}).limit(limit)
        return [self.get_tweets_for_user(user) for user in users_objs]

    def get_trace_for_user(self, username):
        '''
        TODO docstring
        '''
        return self.get_tweets_for_user_str(username)

if __name__ == '__main__':
    client = DBClient()
    #client.create_users_collection()
    client.remove_users_and_tweets(100, 3)
