#!/usr/bin/env python
# coding: utf-8

# In[1]:



# import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:



news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# featured images
# 

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com/'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[12]:



# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[13]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# In[14]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[15]:


df.to_html()


# In[16]:


# 1. Use browser to visit the URL 
url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
browser.visit(url)


# In[18]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
links = browser.find_by_css("a.product-item h3")
for image in range(len(links)):
    try:
        print('Yes')
        hemisphere = {}
        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[image].click()
        # Next, we find the sample image anchor tag and extract the href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        # Get the hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    except Exception as e:
        print('Nope!', e)


# In[19]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[20]:


browser.quit()


# In[ ]:




