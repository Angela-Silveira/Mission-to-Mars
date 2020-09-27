#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[2]:


# Set the executable path and initialize chrome browser
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)


# In[3]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[5]:


slide_elem.find("div", class_='content_title')


# In[6]:


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Image

# In[8]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[10]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[11]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:


# Find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# In[14]:


# Scrape Mars facts table
df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df


# In[15]:


df.to_html()


# In[16]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[17]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[18]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# In[19]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
# Parse the data
html = browser.html
image_soup = soup(html, 'html.parser')


# In[42]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.


# In[43]:


# Retrieve Cerberus enhanced jpg
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


# In[44]:


# Retrieve Schiaparelli enhanced jpg
page_dictionary = {
    "title": title,
    "url": img_url
}
url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
browser.visit(url)
html = browser.html
image_soup = soup(html, 'html.parser')
title = image_soup.find('h2').get_text()
img = image_soup.find_all('img')[5]["src"]
img_url = url + img
hemisphere_image_urls.append(page_dictionary)
print(hemisphere_image_urls)


# In[45]:


# Retrieve Syrtis Major enhanced jpg
page_dictionary = {
    "title": title,
    "url": img_url
}
url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
browser.visit(url)
html = browser.html
image_soup = soup(html, 'html.parser')
title = image_soup.find('h2').get_text()
img = image_soup.find_all('img')[5]["src"]
img_url = url + img
hemisphere_image_urls.append(page_dictionary)
print(hemisphere_image_urls)


# In[46]:


# Retrieve Valles Marineris enhanced jpg
url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
browser.visit(url)
html = browser.html
image_soup = soup(html, 'html.parser')
title = image_soup.find('h2').get_text()
img = image_soup.find_all('img')[5]["src"]
img_url = url + img
hemisphere_image_urls.append(page_dictionary)


# In[47]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[48]:


browser.quit()


# In[ ]:




