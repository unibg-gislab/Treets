import flask
from pymongo import MongoClient

# TODO: manage with os.environ.get
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1Ijoibmljb2xhOTMiLCJhIjoiY2l2Y2ozYnZ5MDBocTJ5bzZiM284NGkyMiJ9.4VUvTxBv0zqgjY7t3JTFOQ'
DEBUG_MODE = True


class Application(flask.Flask):
    """docstring for ClassName"""

    def __init__(self, import_name):
        self.import_name = import_name
        super(Application, self).__init__(import_name)

        self.route('/', methods=['GET', 'POST'])(self.main)
        self.route('/searchText', methods=['GET', 'POST'])(self.search_text)
        self.route('/geo', methods=['GET', 'POST'])(self.search_within_cirle)
        self.routeroute('/export', methods=['GET', 'POST'])(self.export)

        self.mapbox_access_token = MAPBOX_ACCESS_TOKEN
        self.mongo = MongoClient()
        self.db = self.mongo.test
        self.debug = DEBUG_MODE
        self.query_issuer = None  # TODO

    def run(self):
        self.app.run()

    def main(self):
        return flask.render_template('index.html', ACCESS_KEY=self.mapbox_access_token)

    def show_all_tweets(self):
        import pdb
        pdb.set_trace()

    def search_text(self):
        '''
        Search for the input string in the tweets' text
        '''
        words = flask.request.form['src']
        if words:
            return self.query_issuer.search(words)

    def search_within_cirle(self):
        '''
        Search every tweets inside the circle
        center in gps location
        radius given by user
        '''
        # TODO controllare che l'input sia numerico
        lat = flask.request.form['lat']
        lon = flask.request.form['lon']
        radius = flask.request.form['radius']
        message = 'lat: ' + lat + ' lon: ' + lon + ' rad: ' + radius
        if lat == '' or lon == '' or radius == '':
            message = 'campo/i mancante'
        return message

    def export(self):
        return "exporting"

application = Application(__name__)
