
# from IPython import get_ipython

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Path to chromedriver
get_ipython().system('which chromedriver')

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

#################################
# Visit the NASA Mars News Site #
#################################

# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p

###################################
# JPL Space Images Featured Image #
###################################

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

# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel

# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url

##############
# Mars Facts #
##############

df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()

df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df

df.to_html()

################
# Mars Weather #
################

# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)

# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')

# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())

#################################################################
# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles #
#################################################################

###############
# Hemispheres #
###############

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

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()
