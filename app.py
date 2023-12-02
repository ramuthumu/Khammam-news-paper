from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Fetch and parse the HTML content from the URL
def fetch_and_parse_html(url):
    response = requests.get(url)

    print(url,"ksjkkskds")
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all("aside", {"class": "thumb-content-more"}):
        title = article.find("h3", {"class": "fnt20 article-title-rgt"}).text.strip()
        link = article.find("a")["href"]

        image_tag = article.find("img")
        image_url = image_tag["src"] if image_tag else None

        articles.append({"title": title, "link": link, "image_url": image_url})

    return articles

@app.route('/')
def home():
    url = "https://www.eenadu.net/telangana/districts/khammam"
    articles = fetch_and_parse_html(url)
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
