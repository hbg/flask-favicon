from flask import current_app, _app_ctx_stack
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
		self.app = app
		self.sizes = sizes
		self.file = file
		if app is not None and file is not None:
			self.create_favicons(app=app, file=file)
	def init_app(self, app):
		self.app = app
	def create_favicons(self, app, file, *args, **kwargs):
		self.creation_engine(image=file, sizes=self.sizes)
		self.assets = Environment(app)
		self.favicons = Bundle(self.favicon_resources)
		self.assets.register('favicons',self.favicons)
	@property
	def favicons(self):
		return self.favicons
	@property
	def app(self):
		return self.app
	@property
	def sizes(self):
		return self.sizes
	def creation_engine(self, image, sizes):
			for size in sizes:
				try:
					file = Image.open(image)
					file.thumbnail([size[0], size[1]], Image.ANTIALIAS)
					path = os.path.splitext(image)[0] + "{}-{}.ico".format(size[0], size[1])
					file.save(path)
					self.favicon_resources.append(path)
				except FileNotFoundError as e:
					print("Base asset\"{}\" not found".format(file))