from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

MAPBOX_ACCESS_KEY = 'pk.eyJ1Ijoibmljb2xhOTMiLCJhIjoiY2l2Y2ozYnZ5MDBocTJ5bzZiM284NGkyMiJ9.4VUvTxBv0zqgjY7t3JTFOQ'
app.debug = True


@app.route('/', methods=['GET', 'POST'])		
def main():
	return render_template('index.html', ACCESS_KEY=MAPBOX_ACCESS_KEY)

def show_all_tweets():
    import pdb; pdb.set_trace()

@app.route('/searchText', methods=['GET', 'POST'])
def searchText():
	'''
	Search for the input string in the teets' text
	'''
	src = request.form['src']
	message = src
	if src == '':
		message = 'campo mancante'
	return message


@app.route('/geo', methods=['GET', 'POST'])
def geo():
	'''
	Search every tweets inside the circle
	center in gps location
	radius given by user
	'''
	#TODO controllare che l'input sia numerico
	lat = request.form['lat']
	lon = request.form['lon']
	radius = request.form['radius']
	message = 'lat: '+ lat +' lon: '+ lon +' rad: '+ radius
	if lat == '' or lon == '' or radius == '':
		message = 'campo/i mancante'
	return message


@app.route('/export', methods=['GET', 'POST'])
def export():
    return "exporting"


# TODO: put this function in a class
def init():
    app.mongo = MongoClient()
    app.db = app.mongo.test
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    init()
    show_all_tweets()
