from flask# import Flask, render_template, request
from pymongo import MongoClient


class Application(flask.Flask):
    """docstring for ClassName"""

    def __init__(self, import_name, mapbox_access_token, debug=False):
        super(Application, self).__init__(import_name)

        self.route('/', methods=['GET', 'POST'])(self.main)
        self.route('/searchText', methods=['GET', 'POST'])(self.search_text)
        self.route('/geo', methods=['GET', 'POST'])(self.search_within_cirle)
        self.routeroute('/export', methods=['GET', 'POST'])(self.export)

        self.mapbox_access_token = mapbox_access_token
        self.mongo = MongoClient()
        self.db = app.mongo.test
        self.debug = debug

    def run(self):
        self.app.run()

    def main(self):
        return render_template('index.html', ACCESS_KEY=MAPBOX_ACCESS_KEY)

    def show_all_tweets(self):
        import pdb
        pdb.set_trace()

    def search_text(self):
        '''
        Search for the input string in the tweets' text
        '''
        words = request.form['src']
        if words:
            tweets = query_issuer.search(words)

    def search_within_cirle(self):
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
        return message

    def export(self):
        return "exporting"


if __name__ == '__main__':

    init()
