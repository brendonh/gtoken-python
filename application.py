from gtoken import setup

setup.setup()
app = setup.app

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()



