from bs4 import BeautifulSoup
import requests

#try:
response=requests.get("https://www.imdb.com/chart/top/")
soup=BeautifulSoup(response.text,'html.parser')
print(soup)
# except Exception as e:
#     print(e)

movies=soup.find('tbody',class_="lister-list")
for i in movies:
    print(i)