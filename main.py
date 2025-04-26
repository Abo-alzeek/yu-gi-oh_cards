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
url_page_2 = 'https://yugioh.fandom.com/wiki/Special:Ask?limit=500&offset=500&q=%5B%5BMedium%3A%3AGX1%5D%5D&p=mainlabel%3D-20-2D%2Fformat%3Dtable%2Fheaders%3D-20plain%2Fclass%3D-20wikitable-20sortable-20card-2Dlist&po=%3FGX1+number%3D%23%0A%3FEnglish+name+%28linked%29%3DCard%0A%3FGX1+name%3D%27%27GX1%27%27+name%0A%3FGX1+DP+Cost%3D%5B%5BDeck+Cost%7CDP+Cost%5D%5D%0A%3FType%3D%5B%5BType%5D%5D%0A%3FLevel%3D%5B%5BLevel%5D%5D%0A%3FATK%23-%3D%5B%5BATK%5D%5D%0A%3FDEF%23-%3D%5B%5BDEF%5D%5D%0A%3FGX1+Status%3D%5B%5BStatus%5D%5D%0A&sort=&order=asc&eq=no#search'
url2 = 'https://yugioh.fandom.com/wiki/'
large_url = 'https://yugioh.fandom.com/wiki/Special:Ask/-5B-5BMedium::GX1-5D-5D/-3FGX1-20number%3D-23/-3FEnglish-20name-20(linked)%3DCard/-3FGX1-20name%3D-27-27GX1-27-27-20name/-3FGX1-20DP-20Cost%3D-5B-5BDeck-20Cost-7CDP-20Cost-5D-5D/-3FType%3D-5B-5BType-5D-5D/-3FLevel%3D-5B-5BLevel-5D-5D/-3FATK-23-2D%3D-5B-5BATK-5D-5D/-3FDEF-23-2D%3D-5B-5BDEF-5D-5D/-3FGX1-20Status%3D-5B-5BStatus-5D-5D/mainlabel%3D-20-2D/limit%3D700/offset%3D0/format%3Dtable/headers%3D-20plain/class%3D-20wikitable-20sortable-20card-2Dlist'
page = requests.get(url)

def getSubInfo(card: CardData):
    generated_url = f'{url2}{card.card}'
    print("generated_url:", generated_url)
    subPage = requests.get(generated_url)
    soup = BeautifulSoup(subPage.content, "html.parser")

    tables = soup.find_all("table")

    for i in tables:
        if len(i.find_all("tr")):
            table = i
            break
    else:
        print("there's no table with more than 1 rows...")
        return

    rows = table.find_all("tr")

    print("table length:", len(rows))

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
        input("Press Enter to continue:")
        
        if cnt == 1: 
            break
        cnt = cnt + 1


main(page)
