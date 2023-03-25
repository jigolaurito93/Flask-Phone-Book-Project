from flask import Flask

app = Flask(__name__)

# import all of the routes from the routes file into the current package
from . import routes
# or from app  import routes