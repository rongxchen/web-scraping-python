import asyncio
import aiohttp
from aiohttp import ClientSession
from typing import Coroutine, List


async def _requests(session: ClientSession, 
                    method: str, 
                    url: str, 
                    headers: dict, 
                    params: dict = None, 
                    json: dict = None, 
                    data: dict = None):
    if method == "get":
        async with session.get(url=url, params=params, headers=headers) as resp:
            return await resp.json()
    if method == "post":
        async with session.post(url=url, json=json, data=data, headers=headers) as resp:
            return await resp.json()
    if method == "put":
        async with session.put(url=url, json=json, data=data, headers=headers) as resp:
            return await resp.json()
    if method == "delete":
        async with session.delete(url=url, params=params, headers=headers) as resp:
            return await resp.json()
    raise ValueError(f"Unsupported method: {method}")


async def get(session: ClientSession, url: str, headers: dict, params: dict = None):
    return await _requests(session, "get", url, headers, params=params)


async def post(session: ClientSession, url: str, headers: dict, json: dict = None, data: dict = None):
    return await _requests(session, "post", url, headers, json=json, data=data)


async def put(session: ClientSession, url: str, headers: dict, json: dict = None, data: dict = None):
    return await _requests(session, "put", url, headers, json=json, data=data)


async def delete(session: ClientSession, url: str, headers: dict, params: dict = None):
    return await _requests(session, "delete", url, headers, params=params)


def get_session():
    return aiohttp.ClientSession()


def gather_tasks(tasks: List[Coroutine]):
    return asyncio.gather(*tasks)


def run(coroutine: Coroutine):
    return asyncio.run(coroutine)
