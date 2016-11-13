from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return

@app.route("/navigator")
def navigator(search_term:Str):


if __name__ == "__main__":
    app.run()


