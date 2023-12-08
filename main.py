import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3"
}
r = requests.get(
    "https://www.albumoftheyear.org/ratings/user-highest-rated/all/", headers=headers
)

html_content = r.text

soup = BeautifulSoup(html_content, "lxml")

elements = soup.findAll("div", class_="albumListRow")

result = []
for element in elements:
    title = element.find("h2", class_="albumListTitle").text
    score = element.find("div", class_="scoreValue").text
    ratings = element.find("div", class_="scoreText").text

    ratings = "".join(c for c in ratings if c.isdigit())
    if int(ratings) >= 1000:
        result.append([title, score, ratings])

for item in result:
    print(f"Title: {item[0]}, Score: {item[1]}, Ratings: {item[2]}")
