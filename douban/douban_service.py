import pandas as pd
from common.const import DOUBAN_250_URL
from common.http import get_header
from util import aiohttp_util
from aiohttp import ClientSession
from douban import douban_util
from typing import List


async def get_douban_250_one_page(session: ClientSession, page: int):
    print(f"fetching page {page}")
    header = get_header()
    params = {"start": (page - 1) * 25}
    text = await aiohttp_util.get(session=session, url=DOUBAN_250_URL, headers=header, params=params, return_json=False)
    return text


async def get_douban_250():
    lst = []
    async with aiohttp_util.get_session() as session:
        tasks = [get_douban_250_one_page(session, page) for page in range(1, 11)]
        res = await aiohttp_util.gather_tasks(tasks)
        for r in res:
            if r is None or not isinstance(r, str):
                continue
            lst.extend(douban_util.process_douban_250_one_page(r))
    return lst


def save(data_list: List[dict], folder: str):
    path = f"{folder}/douban_top250.csv"
    df = pd.DataFrame(data=data_list)
    df.to_csv(path, index=False)


async def main():
    res = await get_douban_250()
    save(res, "./csv/douban")
    print(len(res))
