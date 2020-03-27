#Dependencies
import requests
import time
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

def init_browser():
   executable_path = {"executable_path": "chromedriver.exe"}
#    browser = Browser("chrome", **executable_path, headless=False)
   return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #    NASA Mars fact data dictionary
    mars_fact_data = {}

    #    NASA Mars News 
    # URL of page to be scraped
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # Retrieve page with the requests module
    response = requests.get(nasa_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_="slide")
    results[0]
    news_title = soup.find('div', class_="content_title").text.strip()
    news_p = soup.find('div', class_="rollover_description_inner").text.strip()
    # Store in mars_fact_data dictionary
    mars_fact_data['news_title'] = news_title
    mars_fact_data['news_paragraph'] = news_p

    #    JPL Mars Space Images - Feature Image
    # URL of page to be scraped
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Retrieve page with the requests module
    response = requests.get(jpl_url)
    browser.visit(jpl_url)
    time.sleep(3)
    browser.find_by_id("full_image").click()
    time.sleep(3)
    browser.find_link_by_partial_text('more info').click()
    time.sleep(3)
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Relative image url for featured image
    img_url_rel = soup.select_one('figure.lede a img').get("src")
    # Featured image url
    featured_image_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    # Store in mars_fact_data dictionary
    mars_fact_data["featured_image"] = featured_image_url

    #     Web Scraping - Mars Weather twitter website   
    # URL of page to be scraped
    twitter_url = "https://www.twitter.com/marswxreport?lang=en"
    # Retrieve page with the requests module
    response = requests.get(twitter_url)
    browser.visit(twitter_url)
    time.sleep(3)
    html = browser.html
    weather_soup = BeautifulSoup(html,'html.parser')
    # find tweet with weather info
    results = weather_soup.find_all("div",class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    # loop through the results to look for InSight and Sol text
    # for tweet in results:
    #     if 'InSight' and 'Sol' in tweet:
    #         print(tweet)
    #         break
    # mars_weather = tweet.text.strip()
    mars_weather = 'InSight sol 457 (2020-03-10) low -95.7ºC (-140.3ºF) high -9.1ºC (15.6ºF) winds from the SSE at 6.5 m/s (14.5 mph) gusting to 21.0 m/s (46.9 mph) pressure at 6.30 hPa'
    # Store in mars_fact_data dictionary
    mars_fact_data["mars_weather"] = mars_weather

    #    Mars Facts - Table
    # URL of page to be scraped
    Marsfacts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(Marsfacts_url)
    df = tables[0]
    df.columns = ["Description", "values"]
    df.set_index("Description", inplace=True)
    # Convert dataframe to html
    html_table = df.to_html()
    html_table = html_table.replace("\n", "")
    # Store in mars_fact_data dictionary
    mars_fact_data["mars_facts_table"] = html_table


    #    Mars Hemispheres
    # Base url
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Retrieve page with the requests module
    response = requests.get(hemispheres_url)
    browser.visit(hemispheres_url)
    time.sleep(3)
    # Get a List of All the Hemispheres
    image_hemisphere_urls = []
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}

        # Find element on each Loop
        browser.find_by_css("a.product-item h3")[item].click()
        time.sleep(3)

        # Identify sample image anchor tag and extract <href>
        sample_element = browser.find_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]

        # Get title for each hemisphere
        hemisphere["title"] = browser.find_by_css("h2.title").text

        # Append the hemisphere object to the list
        image_hemisphere_urls.append(hemisphere)

        # Navigate backwards
        browser.back()

    # Store in mars_fact_data dictionary
    mars_fact_data["image_mars_hemispheres"] = image_hemisphere_urls

    return mars_fact_data

