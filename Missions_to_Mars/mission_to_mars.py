# Mission to Mars
# Set up dependencies - BeautifulSoup, Splinter and Pandas
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# Step 1 - Scraping
# Create the executable path and initialize Splinter/Chrome
from splinter import Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# NASA Mars News

# Scrape the Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.
url = 'https://redplanetscience.com/'
browser.visit(url)

# Assign html object to page
html = browser.html

# Parse html with beautifulSoup
news_soup = soup(html, 'html.parser')
slide_element = news_soup.select_one('div.list_text')

# Find latest NASA `news_title`
news_title = slide_element.find('div', class_='content_title').get_text()
news_title
#print(news_title)
# Find the paragraph text
news_p = slide_element.find('div', class_='article_teaser_body').get_text()
news_p
#print(news_p)

# JPL Mars Space Images - Featured Image

# Visit the url for the Featured Space Image page here:https://spaceimages-mars.com/
img_url = 'https://spaceimages-mars.com'
browser.visit(img_url)

# Find the image url to the full size .jpg image.
full_image_element = browser.find_by_tag('button')[1]
full_image_element.click()

# Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# Search for the relative image url
img_url = img_soup.select_one('img', class_='fancybox-image').get('src')
img_url

# Use the base url to create an featured image url
featured_img_url = f'https://spaceimages-mars.com/{img_url}'
featured_img_url

# Mars Facts

# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
mars_df = pd.read_html('https://galaxyfacts-mars.com/')[0]
mars_df.head()

#print(mars_df)
mars_df.columns=["Description", "Mars", "Earth"]
mars_df.set_index("Description", inplace=True)
mars_df
#print(mars_df)

mars_df.to_html()

# Mars Hemispheres

# Visit the Astrogeology site here (https://marshemispheres.com/) 
mars_hem_url = 'https://marshemispheres.com/'
browser.visit(mars_hem_url)

# Obtain high resolution images for each of Mar's hemispheres.
hemisphere_image_urls = []

# Retrieve the image urls and titles for each hemisphere.
for hem in range(4):
    # Browse through each article by finding each element on each loop.
    browser.links.find_by_partial_text('Hemisphere')[hem].click()   

# Parse the html with BeautifulSoup
html = browser.html
hem_soup = soup(html,'html.parser')    

# Scraping to retrieve imahe title and save into variables
title = hem_soup.find('h2', class_='title').text
img_url = hem_soup.find('li').a.get('href')   

# Add findings into a dictionary and append to the list
hemispheres = {}
hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
hemispheres['title'] = title
hemisphere_image_urls.append(hemispheres)
  
# Go back to main page
browser.back()

# Close browser
browser.quit()   

# Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# Step 2 - MongoDB and Flask Application

# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.
data = {
        'news_title' : news_title,
        'news_pa' : news_p,
        'featured_image' : featured_img_url,
        'facts' : mars_facts(),
        'hemispheres' : img_urls_titles,
        'last_modified' : dt.datetime.now()
