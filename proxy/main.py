from flask import Flask
from routes import blueprint


app = Flask(__name__)
app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(host="127.1.1.1", port=8100, debug=True)
