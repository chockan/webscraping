from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np



URL="https://www.amazon.in/s?k=laptop&crid=2ZKUN6G4T02XU&sprefix=la%2Caps%2C1196&ref=nb_sb_ss_ts-doa-p_1_2"

HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

webpage = requests.get(URL, headers=HEADERS)

print(webpage)
print(webpage.content)
print(type(webpage.content))

soup = BeautifulSoup(webpage.content, "html.parser")

##print(soup)

# #<a class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
#"
links = soup.find_all("a", attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
#print(links)
print(links)
a=links[0].get('href')
#print(a)
product_list="https://www.amazon.in/" + a
print(product_list)

new_webpage=requests.get(product_list,headers=HEADERS)

##print(new_webpage)

new_soup = BeautifulSoup(new_webpage.content, "html.parser")
# print(new_soup)

c=new_soup.find('span',attrs={'id':'productTitle'})
d=new_soup.find('span',attrs={'id':'productTitle'}).text
e=new_soup.find('span',attrs={'id':'productTitle'}).text.strip()
print(c)
print(d)
print(e)

f=new_soup.find('span',attrs={'class':'a-price-whole"'})
print(f)
g=new_soup.find('span',attrs={'class':'a-price-whole'}).text
print(g)
h=g[:-1]
print(h)


k=new_soup.find('span',attrs={'class':'a-icon-alt'})
print(k)

m=new_soup.find('span',attrs={'class':'a-icon-alt'}).text
print(m)
bn=[]
y=new_soup.find('a',attrs={'class':'a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold'})
z=new_soup.find('a',attrs={'class':'review-title-content'}).text



# print(y)
# print(z)
