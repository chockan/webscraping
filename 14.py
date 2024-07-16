from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

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
stocks = []  # Store stocks

for link in links_list:
    try:
        # Retry logic for failed requests
        for attempt in range(3):
            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
            new_webpage.raise_for_status()  # Raise an exception for HTTP errors
            if new_webpage.status_code == 200:
                break
        else:
            continue  # Skip to the next link if all attempts fail

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Check if the title is properly displayed
        title_tag = new_soup.find("span", id="productTitle")
        price_tag = new_soup.find("span", class_="a-price-whole")
        review_tag = new_soup.find("span", class_="a-icon-alt")
        stock_tag = new_soup.find("span", class_="a-size-medium a-color-success")

        if all((title_tag, price_tag, review_tag, stock_tag)):
            title = title_tag.get_text().strip()
            price = price_tag.get_text().strip()
            review = review_tag.get_text().strip()
            stock = stock_tag.get_text().strip()

            # Verify price format
            if price.isalpha():
                prices.append(price)
            else:
                prices.append(None)

            # Verify review format
            if review.startswith(""):
                reviews.append(review)
            else:
                reviews.append(None)

            titles.append(title)
            stocks.append(stock)
        else:
            titles.append(None)
            prices.append(None)
            reviews.append(None)
            stocks.append(None)

    except requests.exceptions.RequestException as e:
        # Skip printing error messages and continue with the next link
        continue

# Ensure the lengths of titles, prices, reviews, and stocks are the same
if len(titles) != len(prices) != len(reviews) != len(stocks):
    raise ValueError("Lengths of titles, prices, reviews, and stocks lists do not match.")

# Combine titles, prices, reviews, and stocks into a list of lists
table_data = [[title, price, review, stock] for title, price, review, stock in zip(titles, prices, reviews, stocks)]

# Headers for the table
headers = ["Title", "Price", "Review", "Stock"]

# Generate the table
table = tabulate(table_data, headers=headers, tablefmt="grid")
print(table)

# Save the table to a text file
with open("amazon_drones_table.txt", "w") as file:
    file.write(table)

print("Table saved successfully.")
