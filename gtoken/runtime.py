import logging
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_envvar('GTOKEN_COMMON_SETTINGS')
app.config.from_envvar('GTOKEN_LOCAL_SETTINGS')

app.wsgi_app = ProxyFix(app.wsgi_app)


if not app.debug:
    # Set up email alert for error
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'admin@gtoken.com',
                               app.config['ADMINS'], 'GToken server had an error')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

# Log go to a file
# Not working
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler(app.config['LOG_DIR'], maxBytes=10, backupCount=5)
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)


# Init Storm store
from storm.locals import Store, create_database
import yaml
from schemup import commands
from schemup.dbs import postgres
from . import models

store = Store.__new__(Store)

database = create_database(app.config['DB'])
store.__init__(database)

pgConn = store._connection._raw_connection
pgSchema = postgres.PostgresSchema(pgConn, dryRun=False)

commands.load('migrations')
commands.upgrade(pgSchema, models.stormSchema)
commands.validate(pgSchema, models.stormSchema)
