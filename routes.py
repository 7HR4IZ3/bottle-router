import types
from .extra import _get, load_module

class Router:
	'''
Router to handle routes
Adds the set namespace to all route set by the class instance

Parameters:
  During Creation:
	base url: '/auth'
	base route: usually Bottle.route or route or <Your Bottle instance>.route
	routes (optional): a list of your app routes
	
  Calling route and new method:
	the default routes arguments i.e path, method, name, function, skip etc

Usage:
	Router.route:
		auth = Router('/auth', route)
		@auth.route(url='/login', method="GET")
		def login():
			...
	
		produces:
			route('/auth/login', method="GET")
			
	
	Router.new and Router.router:
		auth = Router('/auth', route)
		def login():
		   ...
		   
		# Create route
		auth.new(url='/login', func=login, method='POST')
		
		# Instantiate all created routes
		auth.router()

'''
	def __init__(self, baseUrl, app, r=[]):
		self.baseUrl = self._url(baseUrl)
		self.app = app
		self.routes = r
			
	def _url(self, x):
		if len(x) >= 1 and x[0] != '/':
			x = f'/{x}'
		while '//' in x:
			x = str(x).replace('//', '/')
		else:
			return x

	def error(self, code, func):
		self.app.error(code, callback=func)

	def route(self, url='',  *args, **kwargs):
		url = self._url(self.baseUrl+url)
		return self.app.route(url, *args, **kwargs)

	def mount(self, prefix, child):
		self.app.mount(prefix, child)

	def new(self, **config):
		route = {x: config[x] for x in config}
		self.routes.append(route)

	def mnt(self, url):
		self.baseUrl = self._url(url)
		
	def router_v2(self, config=[]):
		routes = config if config != [] else self.routes
		def make(routes, base_url=''):
			for x in routes:
				if type(x) is str:
					base_url = base_url + self._url(x)
				elif type(x) is dict:
					path = _get(data=x, index='url')
					method = _get(data=x, index='method', e='GET')
					name = _get(data=x, index='name')
					apply = _get(data=x, index='apply')
					skip = _get(data=x, index='skip')
					
					func = _get(data=x, index='func')
					url=base_url+self._url(path)
					self.route(url=url, method=method, callback=func, name=name, apply=apply, skip=skip)
				elif type(x) is tuple:
					make(x[1], x[0])
				elif type(x) is list:
					make(x, base_url=base_url)
		make(routes)

	def find_route(self, routes=[], by='url', value='/'):
		routes = routes if routes != [] else self.routes
		def search(routes, url=""):
			for x in routes:
				if type(routes[x]) is tuple:
					if _get(routes[x], 2) == value:
						return f"{url}{x}"
				elif type(routes[x]) is dict:
					return search(routes[x], url=x)
		return search(routes)
	
	def router(self, config=[]):
		routes = config if config != [] else self.routes
				
		def make(routes, base_url=''):
			for x in routes:
				if type(x) is int:
					func = _get(routes[x], 0)
					self.error(int(x), func)
				elif type(routes[x]) is list:
					make(routes[x], x)
				elif type(routes[x]) is tuple:
					func = _get(data=routes[x], index=0)
					method = _get(data=routes[x], index=1, e='GET')
					name = _get(data=routes[x], index=2)
					apply = _get(data=routes[x], index=3)
					skip = _get(data=routes[x], index=4)
					
					url=base_url+self._url(x)
					if type(func) is types.MethodType or types.FunctionType or types.LambdaType:
						self.route(url=url, method=method, callback=func, name=name, apply=apply, skip=skip)
					else:
						self.route(url=url, method=method, callback=func.as_view, name=name, apply=apply, skip=skip)
				elif type(routes[x]) is dict:
					make(routes[x], base_url=base_url+x)
				elif type(routes[x]) is str:
					if "::" in routes[x]:
						app, framework = routes[x].split("::")
					else:
						app = routes[x]
						framework = "bottle"
					self.app.mount(x, get_app(app, framework))
		make(routes)

def get_app(appn, framework):
	if framework == "bottle":
		app = load_module(appn)
		return app.get_app()
	elif framework == "django":
		app = load_module(f"{appn}.wsgi")
		return app.application
	elif framework == 'flask':
		if "." in appn:
			app, ins = appn.split(".")
		else:
			app = appn
			ins = "app"
		app = load_module(app)
		return getattr(getattr(app, ins), "wsgi_app")
	elif framework == "pyramid":
		if "." in appn:
			app, ins = appn.split(".")
		else:
			app = appn
			ins = "app"
		app = load_module(app)
		return getattr(app, ins)