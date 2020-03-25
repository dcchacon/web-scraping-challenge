# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Mongo integration
client = pymongo.MongoClient()
db = client.mars_db
mars_collection = db.mars_fact_data


# create route that renders index.html template
@app.route("/")
def index():
    mars_collection = list(db.mars_collection.find())
    print(mars_collection)
    return render_template("index.html", mars_collection = mars_collection)

@app.route("/scrape")
def scrape():
    db.collection.delete_many({})
    data = scrape_mars.scrape()
    mars_collection.update({}, data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)