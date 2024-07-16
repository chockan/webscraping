from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

import mysql.connector


HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
# The webpage URL
URL="https://www.amazon.in/s?k=drone&crid=208IBUQWLQPDV&sprefix=drone%2Caps%2C210&ref=nb_sb_noss_1"

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

# Soup Object containing all data
soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
links = soup.find_all("a", attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

#print(links)

# # Store the links
links_list = []

# # # Loop for extracting links from Tag Objects
for link in links:
    
    links_list.append(link.get('href'))

#print(links_list)

# d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
titles = []
prices = []
for link in links_list:
    try:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)
        new_webpage.raise_for_status()  # Raise an exception for HTTP errors
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        
        # Check if the title is properly displayed
        title_tag = new_soup.find("span", id="productTitle")
        if title_tag:
            title = title_tag.get_text().strip()
            #print("Title:", title)
            titles.append(title)
            
            # Continue extracting other information

        price_tag = new_soup.find("span", id="a-price-whole")
        if price_tag:
            price = price_tag.get_text().strip()
            prices.append(price)
        else:
            # If the price is not available, append None
            prices.append(None)
        
    except requests.exceptions.RequestException as e:
        # Skip printing error messages and continue with the next link
        continue
# Create a DataFrame from the list of titles
# df = pd.DataFrame({"Title": titles})

# # Save the DataFrame to a CSV file
# #icacls "d:/python course/amazon_data.csv" /grant Everyone:(OI)(CI)F

# try:
#     # Attempt to write DataFrame to CSV file
#     df.to_csv("d:/python course/amazon_data1.csv", index=False)
#     print("Data saved to amazon_data.csv successfully!")
# except PermissionError:
#     print("Permission denied: Cannot write to amazon_data.csv. Check if you have write permissions in this directory.")
# except Exception as e:
#     print("An error occurred:", e)

df = pd.DataFrame({"Title": titles, "Price": prices})

# Save the DataFrame to the same CSV file
try:
    df.to_csv("d:/python course/amazon_data2.csv", index=False)
    print("Data saved to amazon_data1.csv successfully!")
except PermissionError:
    print("Permission denied: Cannot write to amazon_data1.csv. Check if you have write permissions in this directory.")
except Exception as e:
    print("An error occurred:", e)



# # # # Loop for extracting product details from each link 
# for link in links_list:
#     new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

#     print(new_webpage)

#     print(new_webpage.content)

# #     new_soup = BeautifulSoup(new_webpage.content, "html.parser")

# Replace the placeholders with your MySQL database credentials
# mydb = mysql.connector.connect(


#     host="localhost",
#     user="root",
#     password="Yogan",
#     database="db3"

# )

# mycursor = mydb.cursor()

# # Define the table schema
# create_table_query = """
# CREATE TABLE IF NOT EXISTS drone_titles (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     title VARCHAR(255)
# )
# """

# # Execute the query to create the table
# mycursor.execute(create_table_query)


# # Loop through the list of titles and insert each title into the database
# for title in titles:
#     insert_query = "INSERT INTO drone_titles (title) VALUES (%s)"
#     mycursor.execute(insert_query, (title,))

# # Commit the changes
# mydb.commit()

# mycursor.close()
# mydb.close()

