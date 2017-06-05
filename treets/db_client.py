import pymongo
from radnom import uniform


class DBClient(object):
    '''Docstring for DBClient'''

    def __init__(self):
        super(DBClient, self).__init__()
        self.mongo = pymongo.MongoClient()
        self.db = self.mongo.test
        self.db.tweets.create_index([('location', pymongo.GEOSPHERE)])
        self.db.tweets.create_index([('textMessage', 'text')])

    def get_tweets(self, limit=1000):
        '''
        '''
        return self.db.tweets.find().limit(limit)

    def get_random_tweets(self, limit=1000):
        '''
        '''
        lenght = self.db.tweets.find().count()
        return self.db.tweets.find().limit(limit).skip(uniform()*lenght)

    def get_tweets_near_point(self, coords, dist, limit=1000):
        '''
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

    def search_text(self, text):
        '''
        '''
        return self.db.tweets.find({'$text': {'$search': text}})

if __name__ == '__main__':
    c = DBClient()
    import pdb
    pdb.set_trace()
    print len([c.get_tweets()])
