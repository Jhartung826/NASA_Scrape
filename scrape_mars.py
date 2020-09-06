from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
import pandas as pd
import time
import datetime as dt
from datetime import datetime
from selenium.webdriver.chrome.options import Options
    
def scrape():
    executable_path = {"executable_path": "../../chrome_driver/chromedriver.exe"}
    driver = webdriver.Chrome(**executable_path)
    # options = Options()
    # options.add_argument('--headless')
    news_title, news_p = scrape_news(driver, 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
    scraped_data = {
        "News_Title": news_title,
        "News_Description": news_p,
        "Featured_Image": scrape_featured_image("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"),
        "Weather_Report": scrape_weather(driver, "https://twitter.com/marswxreport?lang=en"),
        "Mars_Fact_Table": mars_fact_table("https://space-facts.com/mars/"),
        "Hemispheres": mars_hemispheres('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'),  
        "modified_date": dt.datetime.today().strftime('%x %X')
    }

    driver.quit()
    return scraped_data
def scrape_news(driver, url):
    driver.get(url)
    time.sleep(2)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select_one('ul.item_list li.slide')
    news_title = articles.div.h3.text
    news_p = articles.div.text
    return news_title, news_p

def scrape_featured_image(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    nasa_image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + nasa_image
    return featured_image_url

# a clunky workaround until I get access to twitter API
def scrape_weather(driver, url):
    driver.get(url)
    time.sleep(3)
    weather_html = driver.page_source
    soup = BeautifulSoup(weather_html, 'html.parser')
    mars_weather = soup.article.div
    mars_facts = mars_weather.find_all("div", {'class':["css-901oao", "css-16my406", "r-1qd0xha", "r-ad9z0x", "r-bcqeeo", "r-qvutc0"], 'dir':'auto'})
    mars_facts = mars_facts[3].text.strip()
    return mars_facts

def mars_fact_table(url):
    mars_fact_table = pd.read_html(url)[0]

    mars_fact_table.rename(columns={1: "Facts", 0: 'Dimensions'}, inplace=True)
    return mars_fact_table.to_html(index=False)

def mars_hemispheres(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')
    hemisphere_list = []
    for hem in soup.find_all('h3'):
        hemisphere = {}
        hemisphere["Title"] = hem.get_text()
        title  = hem.get_text()
        hemisphere["Image"] = f"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/{title.replace(' Hemisphere ', '_').replace(' ', '_')}.tif/full.jpg"
        hemisphere_list.append(hemisphere)
    return hemisphere_list  