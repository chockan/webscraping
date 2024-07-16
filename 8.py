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
        price = soup.find("span", attrs={'id':'a-price-whole'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'a-price-whole'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        rating = soup.find("a", attrs={'class':'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("a", attrs={'class':'review-title-content'}).string.strip()
        except:
            review_count = ""	

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("span", attrs={'class':'a-size-medium a-color-success'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available


if __name__ == '__main__':
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    # The webpage URL
    URL="https://www.amazon.in/s?k=gaming+laptop&crid=E2JDBG720HG1&sprefix=gaming%2Caps%2C234&ref=nb_sb_ss_ts-doa-p_2_6"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

    #print(links)

    # Store the links
    links_list = []

    # # Loop for extracting links from Tag Objects
    for link in links:
        
        links_list.append(link.get('href'))

    #print(links_list)

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    # # Loop for extracting product details from each link 
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

        #print(new_webpage)
        #print(new_webpage.content)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # print(new_soup)
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))


        
    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    print(amazon_df)