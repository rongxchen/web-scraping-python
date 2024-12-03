import os
import requests
import pandas as pd
from typing import List
from common.const import WEIBO_SEARCH_URL
from common.http import get_header
from util import list_util, number_util, date_util


MBLOG_DATE_PATTERN = "%a %b %d %H:%M:%S %z %Y"


def _find_card_nine(card: dict):
    if card["card_type"] == 9:
        return card
    if "card_group" in card and list_util.is_not_empty(card["card_group"]):
        return _find_card_nine(card["card_group"][0])
    return None
    
    
def process_mblog(card: dict):
    mblog = card["mblog"]
    user = mblog["user"]
    return {
        "mid": mblog["mid"],
        "original_text": mblog["text"],
        "like_count": number_util.to_number(mblog["attitudes_count"]),
        "comment_count": number_util.to_number(mblog["comments_count"]),
        "repost_count": number_util.to_number(mblog["reposts_count"]),
        "pictures": [
            item["url"] for item in mblog["pics"]
        ] if "pics" in mblog and list_util.is_not_empty(mblog["pics"]) else [],
        "user": {
            "user_id": user["id"],
            "username": user["screen_name"],
            "description": user["description"],
            "gender": user["gender"],
            "profile_url": user["profile_url"],
            "profile_image": user["profile_image_url"],
            "verified": user["verified"],
            "verified_reason": user["verified_reason"],
            "follow_count": number_util.to_number(user["follow_count"]),
            "followers_count": number_util.to_number(user["followers_count"]),
        },
        "source_device": mblog["source"],
        "country": mblog.get("status_country"),
        "province": mblog.get("status_province"),
        "city": mblog.get("status_city"),
        "created_at": date_util.to_datetime(mblog["created_at"], MBLOG_DATE_PATTERN),
    }


def search(keyword: str):
    page_count = 1
    params = {
        "containerid": f"100103type=1&q={keyword}",
        "page_type": "searchall",
        "page": page_count,
    }
    header = get_header()
    resp = requests.get(url=WEIBO_SEARCH_URL, params=params, headers=header)
    cards = resp.json()["data"]["cards"]
    cards = map(_find_card_nine, cards)
    res = []
    for card in cards:
        if card is not None:
            res.append(process_mblog(card))
    return res


def save(data_list: List[dict], folder: str):
    blog_list = []
    user_list = []
    weibo_blog_path = f"{folder}/blog.csv"
    weibo_user_path = f"{folder}/user.csv"
    if os.path.exists(weibo_blog_path):
        blog_df = pd.read_csv(weibo_blog_path)
        blog_list = blog_df.to_dict(orient="records")
    if os.path.exists(weibo_user_path):
        user_df = pd.read_csv(weibo_user_path)
        user_list = user_df.to_dict(orient="records")
    for data in data_list:
        blog_data = {k: v for k, v in data.items() if k not in ["user"]}
        blog_data["user_id"] = data["user"]["user_id"]
        blog_list.append(blog_data)
        user_list.append(data["user"])
    pd.DataFrame(data=blog_list).to_csv(weibo_blog_path, index=False)
    pd.DataFrame(data=user_list).to_csv(weibo_user_path, index=False)
