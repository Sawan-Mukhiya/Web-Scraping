# scraper.py
# Audio Bee Practical Test
# Extracts top 5 entertainment news and Cartoon of the Day from ekantipur.com

import json
from playwright.sync_api import sync_playwright

def bypass_ads(page):
    """Bypass ad pop-ups if they appear"""
    try:
        skip_btn = page.query_selector("button.inter")
        if skip_btn:
            skip_btn.click()
    except Exception:
        return  


def scrape_entertainment(page):
    """Scrape top 5 entertainment articles"""
    articles = []
    try:
        page.goto("https://ekantipur.com", timeout=60000)
        bypass_ads(page)
        page.wait_for_load_state("networkidle")

        # Navigate to Entertainment
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.click("text=मनोरञ्जन")
        page.wait_for_load_state("networkidle")

        # Extract top 5 articles
        cards = page.query_selector_all("div.category-inner-wrapper")[:5]

        # Traverse each card to extract title, image URL, and author
        for card in cards:
            title = card.query_selector("div.category-description h2 a")
            img = card.query_selector("div.category-image img")
            author = card.query_selector("div.author-name a")

            article = {
                "title": title.text_content().strip() if title else None,
                "image_url": img.get_attribute("src") or img.get_attribute("data-src") if img else None,
                "category": "मनोरञ्जन", # I did not find any tags or attributes that specifies the category in entertainment section
                "author": author.text_content().strip() if author else None
            }
            articles.append(article)

    except Exception as e:
        print(f"Error scraping entertainment: {e}")

    return articles


def scrape_cartoon(page):
    """Scrape Cartoon of the Day"""
    cartoon = {}
    try:
        page.goto("https://ekantipur.com", timeout=60000)
        bypass_ads(page)
        page.wait_for_load_state("networkidle")

        # Navigate to cartoon page
        page.click("text=कार्टुन")
        page.wait_for_load_state("networkidle")

        # Extract cartoon elements
        img = page.query_selector("section.cartoon-main-wrapper img")
        caption = page.query_selector("div.cartoon-description p")

        # I decided to split the cartoon-description into title and the author name, as there was no dedicated any
        if caption:
            caption_text = caption.text_content().strip()
            if " - " in caption_text:
                title, author = caption_text.split(" - ", 1) # this statement splits the caption by the first presence of '-'
            else:
                title, author = caption_text, None
        else:
            title, author = None, None

        # Bundles the info into a dictionary
        cartoon = {
            "title": title,
            "image_url": img.get_attribute("src") if img else None,
            "author": author
        }

    except Exception as e:
        print(f"Error scraping cartoon: {e}")

    return cartoon


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        entertainment_news = scrape_entertainment(page)
        cartoon_of_the_day = scrape_cartoon(page)

        data = {
            "entertainment_news": entertainment_news,
            "cartoon_of_the_day": cartoon_of_the_day
        }

        with open("ekantipur-scraper/output.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        browser.close()


if __name__ == "__main__":
    main()