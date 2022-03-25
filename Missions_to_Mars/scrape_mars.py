# ADJUST THE CODE TO USE IN THE APP.PY

from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import request

# Define executables
def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    img_urls_titles = mars_hem(browser)

# Store data in dictionary, close & quit browser after scraping 
    data = {
        'news_title' : news_title,
        'news_pa' : news_p,
        'featured_image' : featured_img_url,
        'facts' : mars_facts(),
        'hemispheres' : img_urls_titles,
        'last_modified' : dt.datetime.now()
    }
    browser.quit()
    return data

# Grab Mars new link
def mars_news(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_element.find('div', class_='content_title').get_text()
        news_p = slide_element.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# Grab space image link
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None 

    img_url = f'https://spaceimages-mars.com/{img_url}'
    return img_url

# Use Pandas to scrape Mars Facts
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

# Rename columns and set index
    df.columns = ['Description','Mars','Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()

# Grab hemisphere link    
def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

# Add hemisphere image, title and append list to dictionary
    hemisphere_image_urls = []
    for hem in range(4):
        browser.links.find_by_partial_text('Hemisphere')[hem].click()
        html = browser.html
        hemi_soup = soup(html, 'html.parser')
        title = hemi_soup.find('h2', class_='title').text
        img_url = hemi_soup.find('li').a.get('href')
        hemispheres = {}
        hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
        hemispheres['title'] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    return hemisphere_image_urls

if __name__ == "__main__":
    print(scrape_all())
