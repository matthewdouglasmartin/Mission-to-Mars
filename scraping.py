# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# Path to chromedriver (macOS users only)
#!which chromedriver

# Set executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser('chrome', executable_path='chromedriver', headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data

############################
# News Title and Paragraph #
############################

def mars_news(browser):

    # Scrape Mars News
    # Vist the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

###################################
# JPL Space Images Featured Image #
###################################

def featured_image(browser):
    # Visit the mars nasa news site
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

    # Add try/exxcept for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        img_url_rel

    except AttributeError:
        return None

    # Use the base URL to creat and absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

##############
# Mars Facts #
##############

def mars_facts():

    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

################################
# Hemisphere Images and Titles #
################################
def hemisphere(browser):
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    # Find the HTML tag that holds all the links to the full-resolution images
    hemisphere_parent = hemisphere_soup.find('div', class_='collapsible results')

    # Find the HTML tag that holds each individual link to the full-resolution images
    hemisphere_child = hemisphere_parent.select('div.description a')

    # Create a for loop
    for tag in hemisphere_child:
        # Select the relative link to the full-size image
        link = tag.get('href')
        # Create full URL
        hemisphere_tag_url = f'https://astrogeology.usgs.gov{link}'
        # Navigate with browser to URL
        browser.visit(hemisphere_tag_url)
        # Parse the HTML
        html = browser.html
        hemi_image_soup = soup(html, 'html.parser')
        # Find the relative image URL
        hemi_rel_img_url = hemi_image_soup.select_one('img.wide-image').get("src")
        # Find the title
        hemi_img_title = hemi_image_soup.select_one('h2.title').text
        # Create absolute URL from relative URL
        hemi_abs_img_url = f'https://astrogeology.usgs.gov{hemi_rel_img_url}'
        # Append the URL list with a dictionary containing the image URL and title
        hemisphere_image_urls.append({"img_url": hemi_abs_img_url, "img_title": hemi_img_title})

    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
