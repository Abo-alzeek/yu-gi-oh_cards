from dataclasses import dataclass
from pprint import pprint
import requests
from bs4 import BeautifulSoup


@dataclass
class CardData:
    card_id: int = None
    card: str = None
    gx1_name: str = None
    dp_cost: int = None
    card_type: str = None
    level: int = None
    ATK: int = None
    DEF: int = None
    status: str = None


url = "https://yugioh.fandom.com/wiki/List_of_Yu-Gi-Oh!_GX_Duel_Academy_cards"
url2 = 'https://yugioh.fandom.com/wiki/'

page = requests.get(url)

def getSubInfo(card: CardData):
    generated_url = f'{url2}{card.card}'
    # print("generated_url:", generated_url)
    subPage = requests.get(generated_url)
    soup = BeautifulSoup(subPage.content, "html.parser")

    tables = soup.find_all("table")
    
    for i in tables:
        if len(i.find_all("tr")) > 1:
            table = i
            break


    rows = table.find_all("tr")

    if len(rows) < 2:
        print("there's no table with more than 1 rows...")
        return

    cells = rows[1].find_all("td")
    link = cells[0].find_all("a")
    image = link[0]['href']

    # theImage = requests.get(image)
    # with open(f"Cards/{card.card}.png", "wb") as f:
    #     f.write(theImage.content)


def main(page):
    src = page.content
    soup = BeautifulSoup(src, "html.parser")

    cards = []
    the_list = []
    table = soup.find("table")
    rows = table.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) != 9:
            continue

        card = CardData(
            card_id=cells[0].text,
            card=cells[1].text,
            gx1_name=cells[2].text,
            dp_cost=cells[3].text,
            card_type=cells[4].text,
            level=cells[5].text,
        )

        cards.append(card)

    cnt = 0
    for thing in cards:
        print(thing.card)
        getSubInfo(thing)
        # input("Press Enter to continue:")
        
        # if cnt == 1: 
        #     break
        # cnt = cnt + 1


main(page)
