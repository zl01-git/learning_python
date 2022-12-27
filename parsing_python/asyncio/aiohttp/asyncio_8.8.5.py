import logging
import sys
from typing import List
import asyncio
import aiohttp
from bs4 import BeautifulSoup


url = "https://parsinger.ru/html/index1_page_1.html"
head_url = "/".join(url.split("/")[:-1]) + "/"


async def get_soup(_url: str) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(_url) as response:
            return BeautifulSoup(await response.text(), "lxml")
            

async def get_nav_menu(_url: str, _head_url: str) -> List[str]:
    soup = await get_soup(_url)
    logger.debug(f"{_url} ok")
    return [_head_url + nav["href"] for nav in soup.find("div", class_="nav_menu").find_all("a")]
    

async def get_pagens(_url: str, _head_url: str) -> List[str]:
    soup = await get_soup(_url)
    logger.debug(f"{_url} ok")
    return [_head_url + pgn["href"] for pgn in soup.find("div", class_="pagen").find_all("a")]


async def get_urls(_url: str, _head_url: str) -> List[str]:
    soup = await get_soup(_url)
    logger.debug(f"{_url} ok")
    return [_head_url + url["href"] for url in soup.find("div", class_="item_card").find_all("a", class_="name_item")]


async def get_price(_url: str) -> int:
    soup = await get_soup(_url)
    price = soup.find("span", id="price").text.split(" ")[0]
    old_price = soup.find("span", id="old_price").text.split(" ")[0]
    stock = soup.find("span", id="in_stock").text.split(": ")[-1]
    result = (int(old_price) - int(price)) * int(stock)
    logger.debug(f"{_url} ok")
    return result    


async def main(_url: str, _head_url: str) -> None:
    nav_menu = await get_nav_menu(_url, _head_url)
    pagens = await asyncio.gather(*[get_pagens(nav, _head_url) for nav in nav_menu])

    urls_tasks = []
    for page in pagens:
        urls_tasks.extend(page)

    urls = await asyncio.gather(*[get_urls(urls, _head_url) for urls in urls_tasks])
    all_urls = []
    for url in urls:
        all_urls.extend(url)

    result_list_task = [get_price(url) for url in all_urls]
    result_list = await asyncio.gather(*result_list_task)
    print(result_list, len(result_list), sum(result_list))
    logger.debug("Done")


if __name__ == "__main__":
    # create logger
    logger = logging.getLogger("log.8.8.5")
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(name)s, %(funcName)s, %(levelname)s, %(asctime)s, %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG) # after set to WARNING
    #

    asyncio.run(main(url, head_url))
