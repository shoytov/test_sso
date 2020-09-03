from init import app
from routes import *

from oauth.blueprint import oauth


app.register_blueprint(oauth, url_prefix='/oauth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)