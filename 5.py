from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np



def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price1 = soup.find("span", attrs={'class':'a-price-whole'}).text.strip()
        price=price1[:-1]

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class':'a-price-whole'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-size-base a-color-base'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("div", attrs={'class':'cr-helpful-text'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("span", attrs={'class':'a-size-medium a-color-success'}).string.strip()
        #available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available









if __name__ == '__main__':
    URL="https://www.amazon.in/s?k=laptop&crid=3RVEO48O3SUUB&sprefix=laptop%2Caps%2C242&ref=nb_sb_ss_ts-doa-p_2_6"

    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(URL, headers=HEADERS)

    #print(webpage)
    # print(webpage.content)
    #print(type(webpage.content))

    soup = BeautifulSoup(webpage.content, "html.parser")

    #print(soup)

    links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

    #print(links)
    links_list = []

    for link in links:
        links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

        #print(new_webpage)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))


    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    dd=amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    print(dd)