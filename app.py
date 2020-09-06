from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdb"
mongo = PyMongo(app)

@app.route("/")
def index():
    NASA = mongo.db.marsdata.find_one()
    return render_template("index.html", NASA=NASA)

@app.route("/scrape")
def scrape():
    NASA = mongo.db.marsdata
    NASA_scrape = scrape_mars.scrape()
    NASA.update({}, NASA_scrape, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)