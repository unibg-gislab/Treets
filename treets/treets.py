#! /urs/bin/python
# coding: utf8
from __future__ import print_function
from flask import Flask, render_template, request, send_from_directory
from db_client import DBClient
from data_converter import DataConverter

app = Flask(__name__)
app.debug = True
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
    """TODO docstring for Treets"""

    def __init__(self):
        super(Treets, self).__init__()
        self.db_client = DBClient()
        self.data_converter = DataConverter()

    def all_tweets(self, limit=10000):
        '''
        TODO docstring
        '''
        self.result = self.db_client.get_tweets(limit)
        return self.tweets_to_geojson(self.result)

    def all_traces(self, limit=100):
        '''
        TODO docstring
        '''
        self.result = self.db_client.get_traces(limit)
        return self.traces_to_geojsons(self.result)

    def search_text(self, text):
        '''
        TODO docstring
        '''
        self.result = self.db_client.get_tweets_for_text(text)
        return self.tweets_to_geojson(self.result)

    def search_user_tweets(self, text):
        '''
        TODO docstring
        '''
        self.result = self.db_client.get_tweets_for_user(text)
        return self.tweets_to_geojson(self.result)

    def search_near_point(self, coords, dist):
        '''
        TODO docstring
        '''
        self.result = self.db_client.get_tweets_near_point(coords, dist)
        return self.tweets_to_geojson(self.result)

    def tweets_to_geojson(self, result):
        '''
        TODO docstring
        '''
        return self.data_converter.tweets_to_feature_collection(result)

    def traces_to_geojsons(self, result):
        '''
        Returns a geojson fìcontaining all traces and a geojson containing all tweets
        '''
        return self.data_converter.traces_to_feature_collection(result)


treets = Treets()


@app.route('/data/tweets.geojson')
def send_geojson():
    return send_from_directory('static/data', 'tweets.geojson')


@app.route('/', methods=['GET', 'POST'])
def main():
    traces, tweets = treets.all_traces()
    # tweets = treets.all_tweets()
    template_args['shown_tweets'] = len(tweets['features'])
    template_args['shown_traces'] = len(tweets['features'])
    template_args['tweets_geojson'] = str(tweets)
    template_args['traces_geojson'] = str(traces)
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
    cursor = treets.search_user_tweets(message)
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

    template_args['shown_tweets'] = found_tweets
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
    app.run(debug=True)

if __name__ == '__main__':
    init()
