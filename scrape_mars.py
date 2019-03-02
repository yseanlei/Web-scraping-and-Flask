#!/usr/bin/env python
# coding: utf-8

# In[16]:
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import pymongo
import time
def scrape():
        #Mars - News
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        newsurl='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
        browser.visit(newsurl)
        time.sleep(5)
        soup=BeautifulSoup(browser.html,"html.parser")
        nasa_news_titles=soup.find_all('div',class_='content_title')
        news_title=nasa_news_titles[0].text.strip()
        news_paras=soup.find_all('div',class_='article_teaser_body')
        news_para=news_paras[0].text.strip()
        nasa_news_titles=soup.find_all('div',class_='content_title')
        news_title=nasa_news_titles[0].text.strip()
        news_paras=soup.find_all('div',class_='article_teaser_body')
        news_para=news_paras[0].text.strip()

        #Mars - Featured Image
        fimgurl='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(fimgurl)
        soup=BeautifulSoup(browser.html,"html.parser")
        browser.click_link_by_partial_text('FULL IMAGE')
        time.sleep(5)
        browser.click_link_by_partial_text('more info')
        soup=BeautifulSoup(browser.html,"html.parser")
        results=soup.find_all('figure',class_='lede')
        image_url=results[0].a['href'].strip()
        browser.click_link_by_partial_href(image_url)
        soup=BeautifulSoup(browser.html,'html.parser')
        results=soup.find_all('img')
        featured_image_url=results[0]['src']


        #Mars - Weather
        weatherurl="https://twitter.com/marswxreport?lang=en"
        response=requests.get(weatherurl)
        soup=BeautifulSoup(response.text,"html.parser")
        result=soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
        mars_weather=result[0].text.split('\n')[0]

        # Mars - Facts
        facturl='https://space-facts.com/mars/'
        tables=pd.read_html(facturl)
        df=tables[0]
        df.columns=["Description",'Values']
        df.set_index('Description', inplace=True)
        dfhtml=df.to_html()
        marsfacthtml=dfhtml.replace('\n','')

        #Mars Hemispheres
        hemiurl="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        executable_path = {'executable_path': 'chromedriver.exe'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(hemiurl)
        soup=BeautifulSoup(browser.html,"html.parser")
        hemiresults=soup.find_all('h3')
        hemi_img_url=[]
        def get_img_url(title):
            browser.visit(hemiurl)
            browser.click_link_by_partial_text(title)
            soup=BeautifulSoup(browser.html,'html.parser')
            results=soup.find_all('div',class_='downloads')
            image_url=results[0].a['href']
            hemi_dict['img_url']=image_url
            
        for i in range(0,len(hemiresults)):
            hemi_dict={}
            title=hemiresults[i].text.strip()
            hemi_dict['title']=title
            get_img_url(title)
            hemi_img_url.append(hemi_dict)
        hemi_img_url

        # put all scraped data into on dict
        Mars_scraped_data={}
        Mars_scraped_data['news_title']=news_title
        Mars_scraped_data['news_para']=news_para
        Mars_scraped_data['featured_image_url']=featured_image_url
        Mars_scraped_data['mars_weather']=mars_weather
        Mars_scraped_data['marsfacthtml']=marsfacthtml
        Mars_scraped_data['hemi_img_url']=hemi_img_url

        #insert everything into MongoDB
        conn = 'mongodb://localhost:27017'
        client = pymongo.MongoClient(conn)
        db = client.mars_db   # see comment below
        db.mars_collection.drop()  #please delete this line along with the above line if your MongoDB starts with no related collection so that nothing needs to be droped first.  
        db = client.mars_db
        collection = db.mars_collection
        collection.insert_one(Mars_scraped_data)





