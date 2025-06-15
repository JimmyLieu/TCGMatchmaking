from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

## TODO: Will need to figure out a way to iterate through all the decklists on the main page and do this for each one.
## Can probably do a for loop to check through all deck table cells 
## This can become a dagster asset to continuously run
url = "https://gumgum.gg/one-piece/decklists/deck/east/op12/c262b270-2ead-42b8-857f-d07e10dc71d5"
driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

title_el = soup.find("h1")
title = title_el.text.strip() if title_el else "No title found"
print(f"🔹 Deck Title: {title}")

card_divs = soup.select("div.w-1\\/3.mb-2")
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

    if card_code:
        cards.append((qty, card_code))

total_cards = sum(qty for qty, _ in cards)
print(f" Found {len(cards)} unique cards, {total_cards} total cards")

with open("decklist_unique.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Deck Title", "Card Quantity", "Card Code"])
    for qty, code in cards:
        writer.writerow([title, qty, code])

with open("decklist_flat.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Deck Title", "Card Code"])
    for qty, code in cards:
        for _ in range(qty):
            writer.writerow([title, code])

print("Saved decklist_unique.csv and decklist_flat.csv")
driver.quit()
