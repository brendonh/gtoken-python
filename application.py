from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.config.from_envvar('GTOKEN_COMMON_SETTINGS')
app.config.from_envvar('GTOKEN_LOCAL_SETTINGS')

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    app.run()

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'admin@gtoken.com',
                               app.config['ADMINS'], 'GToken server had an error')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

@app.route('/')
def hello_world():
    return 'Hello World!'

