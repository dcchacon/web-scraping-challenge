# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Mongo integration
# client = pymongo.MongoClient()
# db = client.mars_db
# collection = db.mars_fact_data

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


# create route that renders index.html template
@app.route("/")
def index():
    mars_collection = list(mongo.db.collection.find())[0]
    print(mars_collection)
    return render_template("index.html", html_mars_collection = mars_collection)

@app.route("/scrape")
def scrape():
    mongo.db.collection.delete_many({})
    data = scrape_mars.scrape()
    mongo.db.collection.update({}, data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)