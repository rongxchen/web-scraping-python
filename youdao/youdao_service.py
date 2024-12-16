from common.const import YOUDAO_TRANSLATE_SUGGEST_URL, YOUDAO_TRANSLATE_ONE_URL
from common.http import get_header
from util import aiohttp_util
from youdao import youdao_util


async def search_suggest(text: str, num: int = 5):
    text = text.strip()
    params = {
        "num": num,
        "ver": "3.0",
        "doctype": "json",
        "cache": "false",
        "le": "en",
        "q": text,
    }
    header = get_header()
    async with aiohttp_util.get_session() as session:
        res = await aiohttp_util.get(session, YOUDAO_TRANSLATE_SUGGEST_URL, headers=header, params=params)
        return youdao_util.process_suggest(res)
    
    
async def translate_one(text: str):
    text = text.strip()
    url = YOUDAO_TRANSLATE_ONE_URL + "doctype=json&jsonversion=4"
    header = get_header()
    data = {
        "q": text,
        "le": "en",
        "t": "9",
        "client": "web",
        "sign": "",
        "keyfrom": "webdict",        
    }
    async with aiohttp_util.get_session() as session:
        res = await aiohttp_util.post(session, url, headers=header, data=data)
        return youdao_util.process_translate_one(res)
        

async def main():
    text = "hello"
    res = await translate_one(text)
    print(res)
