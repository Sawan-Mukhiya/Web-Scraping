from playwright.sync_api import sync_playwright

def scrape_entertainment(page):
    pass

def scrape_cartoon(page):
    pass

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://ekantipur.com")

        browser.close()



if __name__ == "__main__":
    main()
