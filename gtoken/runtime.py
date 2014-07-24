from flask import Flask
from storm.locals import Store

app = Flask(__name__)

store = Store.__new__(Store)

