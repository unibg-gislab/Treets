import flask, flask.views
app = flask.Flask(__name__)

class View(flask.views.MethodView):
	def get(self):
		return flask.render_template('index.html')
	
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