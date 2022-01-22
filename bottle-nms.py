class namespace:
    def __init__(self, base, route):
        self.base = base
        self.route = route
        
    def url(_url, *args, **kwargs):
        return self.route(base+_url, *args, *kwargs)
    
