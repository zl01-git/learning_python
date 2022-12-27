import logging
import sys
from typing import Dict
import asyncio
import aiohttp
from bs4 import BeautifulSoup


url = "https://parsinger.ru/html/index1_page_1.html"
head_url = "/".join(url.split("/")[:-1]) + "/"
total = 0


async def get_soup(_url: str) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(_url) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            logger.debug("ok") #
            return soup


async def make_urls(_head_url: str, _url: str) -> Dict:
    soup = await get_soup(_url)
    nav_menu = soup.find("div", class_="nav_menu").find_all("a")
    all_urls = {lnk.text: [_head_url + lnk["href"]] for lnk in nav_menu}
    for key, value in all_urls.items():
        soup = await get_soup(*value)
        pagen = soup.find("div", class_="pagen").find_all("a")
        for page in pagen:
            link = _head_url + page["href"]
            if all_urls[key][0] != link:
                all_urls[key].append(link)
    logger.debug("ok") #
    return all_urls


async def get_name_price(_url: str):
    global total
    soup = await get_soup(_url)
    names = soup.find_all("a", class_="name_item")
    prices = soup.find_all("p", class_="price")
    for name, price in zip(names, prices):
        print(_url, name.text, price.text)
        total += 1
    

async def main(_head_url: str,_url: str):
    all_urls = await asyncio.gather(make_urls(head_url, url))
    link_list = []
    for urls in all_urls:
        for key, value in urls.items():
            for lnk in value:
                link_list.append(lnk)
    tasks = [get_name_price(url) for url in link_list]
    await asyncio.wait(tasks)

    logger.debug(total)
    logger.debug("Done")


if __name__ == "__main__":
    # create stdout logger
    logger = logging.getLogger("log.parser")
    handler_stdout = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(name)s, %(funcName)s, %(levelname)s, %(asctime)s, %(message)s")
    handler_stdout.setFormatter(formatter)
    logger.addHandler(handler_stdout)
    logger.setLevel(logging.DEBUG) # set level to logging.WARNING
    # 

    asyncio.run(main(head_url, url))
    
    
   

    