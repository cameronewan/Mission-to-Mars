# import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)


    def mars_news(browser):
        # Visit the mars nasa news site
        url = 'https://redplanetscience.com'
        browser.visit(url)
        # Optional delay for loading the page
        browser.is_element_present_by_css('div.list_text', wait_time=1)

        # Convert the brwoser html to a soup object
        html = browser.html
        news_soup = soup(html, 'html.parser')
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Add try/except for error handling
        try:
            slide_elem = news_soup.select_one('div.list_text')
            # Use the parent element to find the first 'a' tag and save it as 'news_title'
            news_title = slide_elem.find('div', class_='content_title').get_text()
            # Use the parent element to find the paragraph text
            news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        except AttributeError:
            return None, None 

        return news_title, news_p

    # ### Featured Images

    def featured_image(browser):
        # Visit URL
        url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
        browser.visit(url)

        # Find and click the full image button
        full_image_elem = browser.find_by_tag('button')[1]
        full_image_elem.click()

        # Parse the resulting html with soup
        html = browser.html
        img_soup = soup(html, 'html.parser')

        try:
            # Find the relative image url
            img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        except AttributeError:
            return None

        # Use the base URL to create an absolute URL
        img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
        
        return img_url

    # ## Mars Facts
    def mars_facts():
        try:
            # use 'read_html' to scrape the facts table into a dataframe
            df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        except BaseException:
            return None 
        # Assign columns and set index of dataframe    
        df.columns=['description', 'Mars', 'Earth']
        df.set_index('description', inplace=True)
        #Convert dataframe into HTML format, add bootstrap
        return df.to_html(classes='table table-striped')

    # Create a function to scrape the hemisphere data that returns the scraped data
    # as a list of dictionaries with the URL string and title of each hemisphere image

    def hemisphere_data(browser):
        url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
        browser.visit(url)
        hemisphere_image_urls = []
        links = browser.find_by_css("a.product-item h3")
        for image in range(len(links)):
            try:
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
                print(e)
        browser.quit()
        return hemisphere_image_urls
    

    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary
    data = [
        {
            'news_title': news_title,
            'news_paragraph': news_paragraph,
            'featured_image': featured_image(browser),
            'facts': mars_facts(),
            'last_modified': dt.datetime.now()
        },
        {
            'hemispheres': hemisphere_data(browser)
        }]

    #Stop webdriver and return data
    browser.quit()
    return data 



print(scrape_all())