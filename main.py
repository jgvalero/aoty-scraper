import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3"
}


class Album:
    def __init__(self, artist, title, score, ratings):
        self.artist = artist
        self.title = title
        self.score = score
        self.ratings = ratings


class Query:
    def __init__(self, year="", genre="", min_score=80, min_ratings=1000):
        self.year = year
        self.genre = genre
        self.min_score = min_score
        self.min_ratings = min_ratings
        self.url = self.generate_url()
        self.list = []

    def generate_url(self):
        if self.year == "" and self.genre == "":
            url = "https://www.albumoftheyear.org/ratings/user-highest-rated/all/"
        elif self.year == "":
            url = f"https://www.albumoftheyear.org/ratings/user-highest-rated/all/{self.genre}/"
        elif self.genre == "":
            url = f"https://www.albumoftheyear.org/ratings/user-highest-rated/{self.year}/"
        else:
            url = f"https://www.albumoftheyear.org/ratings/user-highest-rated/{self.year}/{self.genre}/"
        return url + "{}/"

    def generate_list(self):
        self.list = get_albums(self.url, self.min_score, self.min_ratings)


def get_albums(base_url, min_score, min_ratings):
    page = 1
    albums = []
    with requests.Session() as s:
        while True:
            url = base_url.format(page)
            r = s.get(url, headers=headers)
            print(url)
            html_content = r.text

            soup = BeautifulSoup(html_content, "lxml")
            elements = soup.select("div.albumListRow")

            for element in elements:
                album = parse_album(element)
                if int(album.score) < min_score:
                    return albums
                if int(album.ratings) >= min_ratings:
                    albums.append(album)

            page += 1


def parse_album(element):
    title = element.find("h2", class_="albumListTitle").text
    title = " ".join(title.split()[1:])
    artist, title = title.split(" - ", 1)
    score = element.find("div", class_="scoreValue").text
    ratings = element.find("div", class_="scoreText").text
    ratings = "".join(c for c in ratings if c.isdigit())
    return Album(artist, title, score, ratings)


query = Query(min_score=80)
query.generate_list()
for album in query.list:
    print(
        f"{album.artist} - {album.title} [Score: {album.score}, Ratings: {album.ratings}]"
    )
