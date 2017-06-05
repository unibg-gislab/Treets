import pymongo
from random import uniform


class DBClient(object):
    '''Docstring for DBClient'''

    def __init__(self):
        super(DBClient, self).__init__()
        self.mongo = pymongo.MongoClient()
        self.db = self.mongo.test
        self.db.tweets.create_index([('location', pymongo.GEOSPHERE)])
        self.check_text_index()

    def check_text_index(self):
        try:
            self.db.tweets.create_index([('textMessage', 'text')])
        except:
            print 'converting texts to unicode, this may take a while'

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
        return self.db.tweets.find().limit(limit).skip(uniform()*lenght)

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

    def search_text(self, text, limit=1000):
        '''
        search for tweets containing <text> and returns results
        '''
        return self.db.tweets.find({'$text': {'$search': text}})

    def search_user_tweets(self, user):
        '''
        returns tweets posted by user
        '''
        return self.db.tweets.find({"userName": user})

if __name__ == '__main__':
    c = DBClient()
    t = list(c.get_tweets(1))
    import pdb
    pdb.set_trace()
    #c.get_tweets_near_point([45.693161, 9.5970498], 3000)
