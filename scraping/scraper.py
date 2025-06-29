import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Try this selector for most food blogs
    steps = [
        p.get_text(strip=True)
        for p in soup.select("li, .instructions-section-item, .mntl-sc-block, .recipe-instructions p")
        if len(p.get_text(strip=True)) > 10
    ]

    return {
        "title": soup.title.string.strip() if soup.title else "Untitled Recipe",
        "steps": steps
    }
