from gtoken.runtime import app


if __name__ == '__main__':
    app.run()


@app.route('/')
def hello_world():
    return 'Hello World!'

