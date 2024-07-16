from bs4 import BeautifulSoup # pip install beautifulsoup4 ,pip install requests

import csv
import requests

URL="https://www.flipkart.com/search?q=drone+camera&sid=jek%2Cp31%2Cjnp&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=RECENT&suggestionId=drone+camera%7CDrones&requestId=d77c7dbe-3dba-4932-a13e-4991d89e2312&as-searchtext=drone%20camera"


HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

webpage=requests.get(URL,headers=HEADERS)

#print(webpage)
# print(webpage.content)
# print(type(webpage.content))

soup = BeautifulSoup(webpage.content, "html.parser")

#print(soup)
links = soup.find_all("a", attrs={"class":"CGtC98"})

# #print(links)
# a=links[0].get('href')
# print(a)
# product_list="https://www.flipkart.com" + a
# print("*"*50)
# print(product_list)

# new_webpage=requests.get(product_list,headers=HEADERS)
# new_soup = BeautifulSoup(new_webpage.content, "html.parser")

# b = new_soup.find("span", attrs={"class":"VU-ZEz"})
# c = new_soup.find("span", attrs={"class":"VU-ZEz"}).text     
# d = new_soup.find("div", attrs={"class":"Nx9bqj CxhGGd"}).text
# print(d)
links_list = []
for i in links:
  links_list.append(i.get('href'))

print(links_list)

titles = []
prices = []
reviews = []  # Store reviews
stocks = []

for link in links_list:
    try:
        # Retry logic for failed requests
        for i in range(3):
            new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)
            new_webpage.raise_for_status()  # Raise an exception for HTTP errors
            if new_webpage.status_code == 200:
                break
        else:
            continue  # Skip to the next link if all attempts fail

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Check if the title is properly displayed
        title_tag = new_soup.find("span", attrs={"class":"VU-ZEz"})
        price_tag = new_soup.find("div", attrs={"class":"Nx9bqj CxhGGd"})
        review_tag = new_soup.find("span", attrs={"class":"E3XX7J"})
        stock_tag = new_soup.find("div", attrs={"class":"UkUFwK WW8yVX"})

        if title_tag and price_tag and review_tag and stock_tag:
            title = title_tag.get_text().strip()
            titles.append(title)
            price = price_tag.get_text().strip()
            prices.append(price)
            review = review_tag.get_text().strip()  # Corrected variable name here
            reviews.append(review)  # Corrected variable name here
            stock = stock_tag.get_text().strip()
            stocks.append(stock)
        else:
            titles.append(None)
            prices.append(None)
            reviews.append(None)
            stocks.append(None)


    except requests.exceptions.RequestException as e:
        # Skip printing error messages and continue with the next link
        continue

if len(titles) != len(prices) != len(reviews) != len(stocks):
    raise ValueError("Lengths of titles, prices, reviews, and stocks lists do not match.")

# Combine titles, prices, reviews, and stocks into a list of lists
# Generate table_data
table_data = [[title, price, review, stock] for title, price, review, stock in zip(titles, prices, reviews, stocks)]

# # Iterate through table_data and print each item with label
# for data in table_data:
#     print(" "*20,"\n")
#     print("Title:", data[0],"\n")
#     print("#"*20)
#     print("Price:", data[1],"\n")
#     print("#"*20)
#     print("Review:", data[2],"\n")
#     print("#"*20)
#     print("Stock:", data[3],"\n")
#     print("#"*20)
#     print()  # Print an empty line between each set of data

with open('d:/python course/flipkartdata.csv', 'w', newline='', encoding='utf-8') as file:
  writer = csv.writer(file)
  writer.writerow(["Title", "Price", "Review", "Stock"])
  writer.writerows(table_data)

print("Data has been written to flipkartdata.csv")