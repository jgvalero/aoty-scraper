import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3"
}

base_url = "https://www.albumoftheyear.org/ratings/user-highest-rated/all/{}/"
page = 1
min_score = 90

result = []
stop = False

while not stop:
    url = base_url.format(page)
    r = requests.get(url, headers=headers)
    print(url)
    html_content = r.text

    soup = BeautifulSoup(html_content, "lxml")
    elements = soup.findAll("div", class_="albumListRow")

    for element in elements:
        title = element.find("h2", class_="albumListTitle").text
        title = " ".join(title.split()[1:])
        score = element.find("div", class_="scoreValue").text
        ratings = element.find("div", class_="scoreText").text

        ratings = "".join(c for c in ratings if c.isdigit())
        if int(score) < min_score:
            stop = True
            break
        if int(ratings) >= 1000:
            result.append([title, score, ratings])

    page += 1

for i, item in enumerate(result, start=1):
    print(f"{i}. {item[0]} [Score: {item[1]}, Ratings: {item[2]}]")
