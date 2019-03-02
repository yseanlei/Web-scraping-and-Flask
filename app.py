from flask import Flask, render_template,redirect
from flask_pymongo import PyMongo
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import pymongo
from scrape_mars import scrape
app=Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def pull_present():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db=client.mars_db
    results=db.mars_collection.find()[0]
    news_title=results['news_title']
    news_para=results['news_para']
    featured_image_url=results['featured_image_url']
    mars_weather=results['mars_weather']
    marsfacthtml=results['marsfacthtml']
    title_one=results['hemi_img_url'][0]['title']
    img_url_one=results['hemi_img_url'][0]['img_url']
    title_two=results['hemi_img_url'][1]['title']
    img_url_two=results['hemi_img_url'][1]['img_url']
    title_three=results['hemi_img_url'][2]['title']
    img_url_three=results['hemi_img_url'][2]['img_url']
    title_four=results['hemi_img_url'][3]['title']
    img_url_four=results['hemi_img_url'][3]['img_url']
    return render_template('index.html',news_title=news_title,news_para=news_para,featured_image_url=featured_image_url,
    mars_weather=mars_weather,marsfacthtml=marsfacthtml,title_one=title_one,img_url_one=img_url_one,title_two=title_two,
    img_url_two=img_url_two,title_three=title_three,img_url_three=img_url_three,title_four=title_four,img_url_four=img_url_four)

@app.route("/scrape")
def scrape_store():
    scrape()
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

