from flask import Flask, render_template, request
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

def fetch_article_content(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"title": "Error", "content": "Content not available", "images": []}

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the title
        title = soup.find("h1", class_="red").text.strip() if soup.find("h1", class_="red") else "No Title"

        # Extract the main content
        content_paragraphs = soup.select(".text-justify p")
        content = ' '.join([para.get_text(strip=True) for para in content_paragraphs])

        # Extract images
        images = [img['src'] for img in soup.select(".text-justify img")]

        return {"title": title, "content": content, "images": images}
    except Exception as e:
        return {"title": "Error", "content": "Content not available", "images": []}



@app.route('/')
def home():
    url = "https://www.eenadu.net/telangana/districts/khammam"
    articles = fetch_and_parse_html(url)
    return render_template('index.html', articles=articles)

@app.route('/article')
def article():
    url = request.args.get('url')
    content = fetch_article_content(url)
    return render_template('article.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
