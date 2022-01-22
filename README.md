# Bottle-route-namespace(bottle-nms)
Bottle extension to use namespace to better organize bottle routes

# Usage
Create an instance of the namespace class
Specify the base route and the default route method

``` python
from bottle import route
from bottle-nms import namespace

auth = namespace('/auth', route)

@auth.route('/login')
def login():
    pass

@auth.route('/signup', method="POST")
def signup():
    pass

# produces the routes "/auth/login" and "/auth/signup"
```
