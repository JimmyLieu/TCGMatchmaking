from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

## TODO: Will need to figure out a way to iterate through all the decklists on the main page and do this for each one.
## Can probably do a for loop to check through all deck table cells 
## This can become a dagster asset to continuously run
url = "https://gumgum.gg/?set=west-op11"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

base_url = "https://gumgum.gg"
deck_links = soup.find_all("a", href=lambda x: x and x.startswith("/decklists/deck/"))
deck_urls = [base_url + link["href"] for link in deck_links]

all_decks = []

for deck_url in deck_urls[:5]:
    driver.get(deck_url)
    time.sleep(2)
    deck_soup = BeautifulSoup(driver.page_source, "html.parser")
    title_el = deck_soup.find("h1")
    leader = title_el.text.strip() if title_el else "No title found"
    card_divs = deck_soup.select("div.w-1\\/3.mb-2")
    cards = []
    for card_div in card_divs:
        qty_div = card_div.find("div", class_="font-weight-semibold")
        qty_text = qty_div.text.strip() if qty_div else "1x"
        try:
            qty = int(qty_text.lower().replace("x", "").strip())
        except:
            qty = 1
        picture = card_div.find("picture")
        card_code = None
        if picture:
            source = picture.find("source")
            if source and source.has_attr("srcset"):
                url = source["srcset"]
                card_code = url.split("/")[-1].split(".")[0]
        # Try to get card name (adjust selector as needed)
        name_div = card_div.find("div", class_="text-xs")
        card_name = name_div.text.strip() if name_div else "Unknown"
        if card_code:
            cards.append({"card_code": card_code, "name": card_name, "count": qty})
    all_decks.append({"leader": leader, "cards": cards})
    print(f"Scraped deck: {leader} ({deck_url})")

with open("all_decklists.json", "w") as f:
    json.dump(all_decks, f, indent=2)

print(f"Saved all_decklists.json with {len(all_decks)} decks.")
driver.quit()
