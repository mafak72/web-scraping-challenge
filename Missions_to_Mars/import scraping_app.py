# Dependencies
import scrape_mars
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo

# Create flusk
app = Flask(__name__)

# Apply PyMongo for mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Render index.html
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index2.html", mars=mars)

# Run scrape, update Mongo database using update & redirect to homepage
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({},mars_data, upsert=True)
    return redirect('/', code=302)
    
if __name__ == "__main__":
    app.run(debug=True)
