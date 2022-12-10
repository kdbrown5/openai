from werkzeug.wsgi import DispatcherMiddleware
from App import app

if __name__ == "__main__":
    app.run()