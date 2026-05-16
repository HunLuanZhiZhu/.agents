import requests
from bs4 import BeautifulSoup

r = requests.get('https://huggingface.co/papers', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
articles = soup.find_all('article', limit=3)

for i, a in enumerate(articles):
    print(f"=== Article {i} ===")
    h3 = a.find('h3')
    if h3:
        title_link = h3.find('a')
        if title_link:
            print(f"Title: {title_link.text.strip()}")
            print(f"Link: {title_link.get('href', 'N/A')}")

    # Find vote/like count
    vote_elem = a.find('a', href=lambda x: x and 'arxiv' in x.lower() if x else False)
    if vote_elem:
        # Get the text near the SVG icon
        spans = vote_elem.find_all('span')
        for span in spans:
            text = span.text.strip()
            if text.isdigit():
                print(f"Votes: {text}")
                break

    print()