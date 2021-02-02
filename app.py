from api import app

app.config['DEBUG'] = True

app.run(port=5001)
