from __future__ import print_function
from flask import Flask, render_template, request, send_from_directory
from db_client import DBClient
from data_converter import DataConverter

app = Flask(__name__)
app.debug = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

template_args = {}


MAPBOX_ACCESS_KEY = 'pk.eyJ1Ijoibmljb2xhOTMiLCJhIjoiY2l2Y2ozYnZ5MDBocTJ5bzZiM284NGkyMiJ9.4VUvTxBv0zqgjY7t3JTFOQ'
TWEETS_GEOJSON_FILE = 'treets/static/data/tweets.geojson'


def prefix_route(route_function, prefix='', mask='{0}{1}'):
    '''
      Defines a new route function with a prefix.
      The mask argument is a `format string` formatted with, in that order:
        prefix, route
    '''
    def newroute(route, *args, **kwargs):
        '''New function to prefix the route'''
        return route_function(mask.format(prefix, route), *args, **kwargs)
    return newroute

if __name__ == '__main__':
    app.route = prefix_route(app.route, '/treets')


class Treets(object):
    """docstring for Treets"""

    def __init__(self):
        super(Treets, self).__init__()
        self.db_client = DBClient()
        self.data_converter = DataConverter()

    def all_tweets(self, limit=10000):
        '''
        '''
        self.result = self.db_client.get_tweets(limit)
        return self.result_to_geojson()

    def search_text(self, text):
        '''
        '''
        self.result = self.db_client.get_tweets_for_text(text)
        if not self.result.count():
            print('no result')
            return

    def search_user(self, text):
        '''
        '''
        self.result = self.db_client.get_tweets_for_user(text)
        if not self.result.count():
            print('no result')
            return
        else:
            return

    def search_near_point(self, coords, dist):
        '''
        '''
        self.result = self.db_client.get_tweets_near_point(coords, dist)
        return self.result_to_geojson()

    def result_to_geojson(self, result=None):
        if not result:
            result = self.result
        if not result.count():
            return
        else:
            feature_collection = self.data_converter.tweets_to_feature_collection(
                result)
            return feature_collection


treets = Treets()


@app.route('/data/tweets.geojson')
def send_geojson():
    return send_from_directory('static/data', 'tweets.geojson')


@app.route('/', methods=['GET', 'POST'])
def main():
    template_args['tweets_geojson'] = str(treets.all_tweets(limit=1000))
    return render_template('index.html', template_args=template_args)


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
    cursor = treets.search_text(message)
    result = '...'+str(cursor.count())+'...'
    for tweet in cursor:
        result = result + '\n' + str(tweet)
    return result


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
    return render_template('index.html', template_args=template_args)


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
    # FIXME: check input with js and alert errors
    # if is_number(lat) and is_number(lon) and is_number(radius) and lat != ''
    # and lon != '' and radius != '':

    res = treets.search_near_point(
        [float(lon), float(lat)], float(radius)*1000)

    if res is not None:
        found_tweets = len(res['features'])
        tweets_geojson = res
    else:
        found_tweets = 'NO RESULTS!!!'
        tweets_geojson = template_args['tweets_geojson']

    template_args['found_tweets'] = found_tweets
    template_args['tweets_geojson'] = tweets_geojson

    return render_template('index.html', template_args=template_args)


@app.route('/export', methods=['GET', 'POST'])
def export():
    return "exporting"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def init():
    app.run(debug=False)

if __name__ == '__main__':
    init()
