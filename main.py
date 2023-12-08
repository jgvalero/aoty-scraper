import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3"
}

base_url = "https://www.albumoftheyear.org/ratings/user-highest-rated/all/{}/"
min_score = 80


def get_albums():
    page = 1
    with requests.Session() as s:
        stop = False
        while not stop:
            url = base_url.format(page)
            r = s.get(url, headers=headers)
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
                    yield title, score, ratings

            page += 1


filename = f"min_score_{min_score}.txt"
with open(filename, "w") as f:
    for i, (title, score, ratings) in enumerate(get_albums(), start=1):
        line = f"{i}. {title} [Score: {score}, Ratings: {ratings}\n"
        print(line, end="")
        f.write(line)

print(f"Results also written to {filename}")
