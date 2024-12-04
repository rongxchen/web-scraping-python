import os
import pandas as pd
from aiohttp import ClientSession
from typing import List
from common.const import WEIBO_SEARCH_URL
from common.http import get_header
from util import list_util, number_util, date_util, aiohttp_util


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
    
def process_result(cards: List[dict]):
    res = []
    for card in cards:
        card_nine = _find_card_nine(card)
        if card_nine is not None:
            res.append(process_mblog(card_nine))
    return res


async def search_one_page(session: ClientSession, keyword: str, page: int):
    print(f"fetching page {page} for keyword {keyword}")
    params = {
        "containerid": f"100103type=1&q={keyword}",
        "page_type": "searchall",
        "page": page,
    }
    header = get_header()
    return await aiohttp_util.get(session=session, url=WEIBO_SEARCH_URL, params=params, headers=header)


async def search(keyword: str, page_count: int = 1):
    lst = []
    async with aiohttp_util.get_session() as session:
        tasks = [
            search_one_page(session, keyword, page)
        for page in range(1, page_count+1)]
        res = await aiohttp_util.gather_tasks(tasks)
        for r in res:
            if r is None or not isinstance(r, dict):
                continue
            lst.extend(process_result(r["data"]["cards"]))
        return lst


def save(data_list: List[dict], folder: str, keyword: str):
    blog_list = []
    user_list = []
    weibo_blog_path = f"{folder}/blog-{keyword}.csv"
    weibo_user_path = f"{folder}/user-{keyword}.csv"
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
    data_list = list_util.remove_duplicates(blog_list, key="mid")
    user_list = list_util.remove_duplicates(user_list, key="user_id")
    pd.DataFrame(data=blog_list).to_csv(weibo_blog_path, index=False)
    pd.DataFrame(data=user_list).to_csv(weibo_user_path, index=False)


async def main():
    keyword = "tsla"
    res = await search(keyword, 50)
    save(res, "./csv/weibo", keyword)
