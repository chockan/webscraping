from bs4 import BeautifulSoup
import requests
import pandas as pd

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}

# The webpage URL
URL = "https://www.amazon.in/s?k=drone&crid=208IBUQWLQPDV&sprefix=drone%2Caps%2C210&ref=nb_sb_noss_1"

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

# Soup Object containing all data
soup = BeautifulSoup(webpage.content, "html.parser")

# Fetch links as List of Tag Objects
links = soup.find_all("a", attrs={"class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

# Store the links
links_list = []

# Loop for extracting links from Tag Objects
for link in links:
    links_list.append(link.get('href'))

titles = []
prices = []  # Store prices
reviews = []  # Store reviews

for link in links_list:
    try:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_webpage.raise_for_status()  # Raise an exception for HTTP errors
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Check if the title is properly displayed
        title_tag = new_soup.find("span", id="productTitle")
        price_tag = new_soup.find("span", class_="a-price-whole")
        review_tag = new_soup.find("span", class_="a-icon-alt")

        if title_tag and price_tag and review_tag:
            title = title_tag.get_text().strip()
            titles.append(title)
            price = price_tag.get_text().strip()
            prices.append(price)
            review= review_tag.get_text().strip()
            reviews.append(review)
        else:
            titles.append(None)
            prices.append(None)
            reviews.append(None)

        # Check if the price is available
        # price_tag = new_soup.find("span", attrs={'class':'a-price-whole'})
        # if price_tag:
        #     price = price_tag.get_text().strip()
        #     prices.append(price)
        # else:
        #     # If the price is not available, append None
        #     prices.append(None)

    except requests.exceptions.RequestException as e:
        # Skip printing error messages and continue with the next link
        continue

# Ensure the lengths of titles and prices are the same
if len(titles) != len(prices) != len(reviews):
    raise ValueError("Lengths of titles and prices lists do not match.")

#############################################################
from tabulate import tabulate

# Combine titles and prices into a list of lists
table_data = [[title, price,review] for title, price, review in zip(titles, prices, reviews)]

# Headers for the table
headers = ["Title", "Price","Review"]

# Generate the table
table = tabulate(table_data, headers=headers, tablefmt="grid")
print(table)
# Save the table to a text file
with open("amazon_drones_table.txt", "w") as file:
    file.write(table)

print("Table saved successfully.")


# # Create a DataFrame from the list of titles and prices
# df = pd.DataFrame({"Title": titles, "Price": prices})

# # Save the DataFrame to the same CSV file
# try:
#     df.to_csv("d:/python course/amazon_data4.csv", index=False)
#     print("Data saved to amazon_data1.csv successfully!")
# except PermissionError:
#     print("Permission denied: Cannot write to amazon_data4.csv. Check if you have write permissions in this directory.")
# except Exception as e:
#     print("An error occurred:", e)
