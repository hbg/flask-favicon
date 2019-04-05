from flask import current_app, _app_ctx_stack, Flask, render_template
from flask_assets import Environment, Bundle
import os
from PIL import Image
class Favicon(object):
	"""
	TO DO LIST:
	- Add sitemap xml for favicons
	- Add easy entry into template?
	- Add theme colors
	- Separate folder for favicons
	"""
	favicon_resources = []
	def __init__(self, app=None, file=None, sizes=[(16,16), (32,32),(64,64)], *args, **kwargs):
		self.file = file
		if app is not None and file is not None:
			self.create_favicons(app=app, file=file, sizes=sizes)
	def init_app(self, app):
		self.app = app
	def create_favicons(self, app, file, sizes, *args, **kwargs):
		self.creation_engine(image=file, sizes=sizes)
		assets = Environment(app)
		favicons = Bundle(*self.favicon_resources)
		assets.register('favicons',favicons)
	def creation_engine(self, image, sizes):
			for size in sizes:
				try:
					file = Image.open(image)
					file.thumbnail([size[0], size[1]], Image.ANTIALIAS)
					path = "static/favicon" + "{}-{}.ico".format(size[0], size[1])
					file.save(path)
					self.favicon_resources.append(path.split('static/')[1])
				except FileNotFoundError as e:
					print("Base asset\"{}\" not found".format(self.file))
	def color_scheme(self, color):
		self.color_templates = Bundle()
app = Flask(__name__)
favicon = Favicon(app=app, file="static/sc-transparent.png")

@app.route('/')
def index():
	return render_template('index.html')
if __name__ == '__main__':
     app.run(debug=True)