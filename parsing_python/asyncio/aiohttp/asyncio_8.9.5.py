# import sys
# import logging
from typing import List, Tuple
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from lg import log


url = "https://parsinger.ru/asyncio/aiofile/2/index.html"
head_url = "/".join(url.split("/")[:-1]) + "/"


# @log
async def get_soup(_session: aiohttp.ClientSession, _url: str) -> BeautifulSoup:
    async with _session.get(_url) as response:
        return BeautifulSoup(await response.text(), "lxml")


# @log
async def get_url_list(_session: aiohttp.ClientSession, _url: str, _head_url: str) -> List[str]:
    soup = await get_soup(_session, _url)
    urls = soup.find("div", class_="item_card").find_all("a", class_="lnk_img")
    return [_head_url + lnk["href"] for lnk in urls]



async def main(_url: str, _head_url: str):
    async with aiohttp.ClientSession() as session:
        urls = await get_url_list(session, _url, _head_url)
        print(urls)
        

if __name__  == "__main__": 
    # # logger
    # logger = logging.getLogger(__file__.split("/")[-1])
    # handler = logging.StreamHandler(sys.stdout)
    # formatter = logging.Formatter("%(name)s, %(funcName)s, %(levelname)s, %(asctime)s, %(message)s")
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # logger.setLevel(logging.DEBUG)
    # #

    asyncio.run(main(url, head_url))
