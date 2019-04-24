from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import selenium
from selenium import webdriver

def scrape():
    executable_path = {"executable_path": "C:\\Users\\Jeffh\\Documents\\Bootcamp\\chrome_driver\\chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    Image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    weather_url = "https://twitter.com/marswxreport?lang=en"
    facts_url = "https://space-facts.com/mars/"
    
    NASA_data = {}
    
    mars_facts = []
    mars_categories = []
    nasa_links = []
    nasa_pic_list = []

    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    browser.visit(Image_url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    nasa_image = soup.find("img", class_="thumb")["src"]

    featured_image_url = "https://www.jpl.nasa.gov" + nasa_image

    browser.visit(weather_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_facts = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    browser.visit(facts_url)
    html = browser.html

    mars_fact_table = pd.read_html(facts_url)[0]
    mars_fact_table_modified = pd.data

    driver = webdriver.Chrome()

    driver.get('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
        
    for i in range(1,5):
        print(i)
        nasa_link = driver.find_element_by_xpath(f'//*[@id="product-section"]/div[2]/div[{i}]/div/a')
        nasa_links.append(nasa_link.text)
        nasa_link.click()
        nasa_pic = driver.find_element_by_xpath('//*[@id="wide-image"]/div/ul/li[1]/a').text
        nasa_pic_list.append(nasa_pic)
        driver.execute_script("window.history.go(-1)")
    nasa_df = pd.DataFrame({"Title": nasa_links, "img_url": nasa_pic_list})
    nasa_df
    
    NASA_data
    NASA_data["Title"] = news_title
    NASA_data["Summary"] = news_p
    NASA_data["Image"]=featured_image_url
    NASA_weather
    return NASA_data