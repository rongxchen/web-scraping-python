import requests
from common.const import WEIBO_SEARCH_URL
from common.http import get_header
from util import list_util


def _find_card_nine(card: dict):
    if card["card_type"] == 9:
        return card
    if "card_group" in card and list_util.is_not_empty(card["card_group"]):
        return _find_card_nine(card["card_group"][0])
    return None
    

def search(keyword: str):
    url = f"{WEIBO_SEARCH_URL}"
    page_count = 1
    params = {
        "containerid": f"100103type=1&q={keyword}",
        "page_type": "searchall",
        "page": page_count,
    }
    header = get_header()
    resp = requests.get(url=url, params=params, headers=header)
    cards = resp.json()["data"]["cards"]
    cards = map(_find_card_nine, cards)
    
    for card in cards:
        print(card)
