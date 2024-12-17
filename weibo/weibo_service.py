import os
import pandas as pd
from aiohttp import ClientSession
from typing import List
from common.const import WEIBO_SEARCH_URL
from common.http import get_header
from util import list_util, aiohttp_util
from weibo import weibo_util


def process_result(cards: List[dict]):
    res = []
    for card in cards:
        card_nine = weibo_util.find_card_nine(card)
        if card_nine is not None:
            res.append(weibo_util.process_mblog(card_nine))
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
        tasks = [search_one_page(session, keyword, page) for page in range(1, page_count+1)]
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
