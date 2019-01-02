import configparser
from klein import Klein

app = Klein()
resource = app.resource

config = configparser.ConfigParser()
config.read('config.ini')
