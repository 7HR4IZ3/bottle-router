class namespace:
    def __init__(self, base, route):
        self.base_url = base
        self.base_route = route
        
    def route(self, url, *args, **kwargs):
        return self.base_route(self.base_url+url, *args, *kwargs)
    
