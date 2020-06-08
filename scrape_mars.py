from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    news_url = 'https://mars.nasa.gov/news/'
    news_response = requests.get(news_url)
    news_soup = BeautifulSoup(news_response.text, 'html.parser')
    news_title = news_soup.find('div', class_='content_title').find('a').text.strip()
    news_p = news_soup.find('div', class_='rollover_description_inner').text.strip()

    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text('more info')
    featured_image_html = browser.html
    featured_image_soup = BeautifulSoup(featured_image_html, 'html.parser')
    featured_image_url = featured_image_soup.find('figure', class_='lede').find('a')['href']
    full_featured_image_url = "https://www.jpl.nasa.gov" + featured_image_url
    
    fact_url = 'https://space-facts.com/mars/'
    fact_table = pd.read_html(fact_url)[0]
    fact_table.rename(columns={0: "Description", 1: "Value"},inplace=True)
    fact_table.set_index('Description', inplace=True)
    fact_table_html = fact_table.to_html()
    fact_table_html.replace('\n', '')

    mars_hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    mars_hemi_response = requests.get(mars_hemi_url)
    mars_hemi_soup = BeautifulSoup(mars_hemi_response.text, 'html.parser')
    hemi_image_urls = []
    results = mars_hemi_soup.find_all('div', class_='item')
    
    for result in results:
        image_title = result.find('h3').text
        image_url = result.find('a', class_='itemLink product-item')['href']
        full_image_url = "https://astrogeology.usgs.gov/" + image_url
        browser.visit(full_image_url)
        each_hemi_html = browser.html
        each_hemi_soup = BeautifulSoup(each_hemi_html, 'html.parser')
        each_hemi_url = each_hemi_soup.find('div', class_="downloads").find('a')['href']
        post = {
            'title': image_title, 
            'img_url': each_hemi_url,
        }
        hemi_image_urls.append(post)


    listings["news_title"] = news_title
    listings["news_p"] = news_p
    listings["featured_image_url"] = full_featured_image_url
    listings["fact_table"] = fact_table_html
    listings["hemi"] = hemi_image_urls

    return listings
