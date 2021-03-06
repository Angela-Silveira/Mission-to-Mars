# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dict
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(), 
        "hemispheres": hemisphere_data()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert browser html to soup object and then quit
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        # Use parent element to find first 'a' tag and save as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None 

    return news_title, news_p

    # Scrape Mars hemisphere images & titles

# ### Featured Image
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None 

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url 

# Scrape Mars facts table
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None 

    # Assign columns and set index
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Convert dataframe to HTML format, add bootstrap
    return df.to_html()(classes="table table-striped")

# Scrape URL/title for each hemisphere image
def hemisphere_data():
    hemisphere_image_urls = []
    page_dictionary = {
        "title": title,
        "url": img_url
    }
    
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser.visit(url)
    html = browser.html
    image_soup = soup(html, 'html.parser')
    title = image_soup.find('h2').get_text()
    img = image_soup.find_all('img')[5]["src"]
    img_url = url + img
    hemisphere_image_urls.append(page_dictionary)
    
    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser.visit(url)
    html = browser.html
    image_soup = soup(html, 'html.parser')
    title = image_soup.find('h2').get_text()
    img = image_soup.find_all('img')[5]["src"]
    img_url = url + img
    hemisphere_image_urls.append(page_dictionary)

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser.visit(url)
    html = browser.html
    image_soup = soup(html, 'html.parser')
    title = image_soup.find('h2').get_text()
    img = image_soup.find_all('img')[5]["src"]
    img_url = url + img
    hemisphere_image_urls.append(page_dictionary)

    url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser.visit(url)
    html = browser.html
    image_soup = soup(html, 'html.parser')
    title = image_soup.find('h2').get_text()
    img = image_soup.find_all('img')[5]["src"]
    img_url = url + img
    hemisphere_image_urls.append(page_dictionary)

    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



