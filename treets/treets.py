from __future__ import print_function
from flask import Flask, render_template, request
from db_client import DBClient
from data_converter import DataConverter


app = Flask(__name__)
app.debug = True
MAPBOX_ACCESS_KEY = 'pk.eyJ1Ijoibmljb2xhOTMiLCJhIjoiY2l2Y2ozYnZ5MDBocTJ5bzZiM284NGkyMiJ9.4VUvTxBv0zqgjY7t3JTFOQ'


class Treets(object):
    """docstring for Treets"""

    def __init__(self):
        super(Treets, self).__init__()
        self.db_client = DBClient()
        self.data_converter = DataConverter()

    def search_text(self, text):
        '''
        '''
        self.result = self.db_client.get_tweets_for_text(text)
        # check if not empty result
        # export result to geojson
        # add geojson to mapbox

    def search_user(self, text):
        '''
        '''
        self.result = self.db_client.get_tweets_for_user(text)
        # check if not empty result
        # export result to geojson
        # add geojson to mapbox

    def search_near_point(self, coords, dist):
        '''
        '''
        self.result = self.db_client.get_tweets_near_point(coords, dist)
        # check if not empty result
        # export result to geojson
        # add gejson to mapbox


treets = Treets()


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html', ACCESS_KEY=MAPBOX_ACCESS_KEY)


def show_all_tweets():
    import pdb
    pdb.set_trace()


@app.route('/searchText', methods=['GET', 'POST'])
def searchText():
    '''
    Search for the input string in the teets' text
    '''
    src = request.form['src']
    message = src
    if src == '':
        message = 'campo mancante'

    result = 'OOO'
    cursor =  treets.search_text(message)
    result = '...'+str(cursor.count())+'...'
    for tweet in cursor:
        result = result + '\n' + str(tweet)
        print tweet
    return result
    # TODO show tweets

    # Conflicts below
    # str(app.mongo.test.collection_names(include_system_collections=False))
    # textMessage

    #    '''
    #    mrcl_zm ha 7 tweets
    #    carpoolworld ne ha 25800
    #    Gus141998 ne ha 1

    #    for tweet in app.mongo.test.tweets.find({"userName": "mrcl_zm"}):
    #    messsage = message + str(tweet)
    #    '''
    # #db_client.search_text(message)
    # #db_client.get_tweets_near_point([45.701322, 9.662846], 6000).count()
    # #app.mongo.test.tweets.find_one({"textMessage": "El nuevo uniforme de la #Vinotinto. Ustedes juzguen... http://t.co/GL7XcTejXZ"})
    # #str(app.mongo.test.tweets.find({"geo": [ 38.80054799, -9.14410241 ]}).count())
    # #app.mongo.test.tweets.find_one({"textMessage": {'$regex': "obrigada"}})
    # #message + str(app.mongo.test.tweets.find({"userName": "mrcl_zm"}).count())
    #    return message
	
	
@app.route('/searchUser', methods=['GET', 'POST'])
def searchUser():
    '''
    Search for the user
    '''
    src = request.form['src']
    message = src
    if src == '':
        message = 'campo mancante'
    result = 'OOO'
    cursor = treets.search_user(message)
    result = '...'+str(cursor.count())+'...'
    for tweet in cursor:
        result = result + '\n' + str(tweet)
        print tweet
    return result


@app.route('/geo', methods=['GET', 'POST'])
def geo():
    '''
    Search every tweets inside the circle
    center in gps location
    radius given by user
    '''
    # TODO controllare che l'input sia numerico
    lat = request.form['lat']
    lon = request.form['lon']
    radius = request.form['radius']
    message = 'lat: ' + lat + ' lon: ' + lon + ' rad: ' + radius
    if lat == '' or lon == '' or radius == '':
        message = 'campo/i mancante'
    result = 'OOO'
    cursor = treets.search_near_point([float(lat), float(lon)], float(radius)*1000)
    result = '...'+str(cursor.count())+'...'
    for tweet in cursor:
        result = result + '\n' + str(tweet)
        print tweet
    return result


@app.route('/export', methods=['GET', 'POST'])
def export():
    return "exporting"


# TODO: put this function in a class
def init():
    app.run()

if __name__ == '__main__':
    init()
