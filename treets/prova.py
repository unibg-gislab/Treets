import flask
import flask.views
app = flask.Flask(__name__)

MAPBOX_ACCESS_KEY = 'pk.eyJ1Ijoibmljb2xhOTMiLCJhIjoiY2l2Y2ozYnZ5MDBocTJ5bzZiM284NGkyMiJ9.4VUvTxBv0zqgjY7t3JTFOQ'


class View(flask.views.MethodView):

    def get(self):
        return flask.render_template('index.html', ACCESS_KEY=MAPBOX_ACCESS_KEY)

    def post(self):
        return "Works!"


@app.route('/searchText', methods=['GET', 'POST'])
def searchText():
    return "searching..."


@app.route('/geo', methods=['GET', 'POST'])
def geo():

    return "cirlce O"


@app.route('/export', methods=['GET', 'POST'])
def export():
    return "exporting"

app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])


app.debug = True
app.run()
