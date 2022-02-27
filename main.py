class Router:
    '''
Router to handle routes
Adds the set namespace to all route set by the class instance

Parameters:
  During Creation:
    base url: '/auth'
    bass route: Bottle.route or route or <Your Bottle instance>.route
    routes: a list of your app routes
  Calling route method:
    the default routes arguments

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

'''
    def __init__(self, baseUrl, base_route, r=[]):
        self.baseUrl = self._url(baseUrl)
        self.base_route = base_route
        self.routes = r
            
    def _url(self, x):
        if len(x) >= 1 and x[0] != '/':
            x = f'/{x}'
        while '//' in x:
            x = str(x).replace('//', '/')
        else:
            return x
        
    def route(self, url='',  *args, **kwargs):
        url = self._url(self.baseUrl+url)
        return self.base_route(url, *args, **kwargs)
        
    def new(self, **config):
        route = {x: config[x] for x in config}
        self.routes.append(route)
        
    def router(self, config=[]):
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
                elif type(x) is list:
                    make(x, base_url=base_url)
        make(routes)
