from pymongo import MongoClient
import  flask


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
        self.db = self.mongo.test
        self.debug = debug

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
