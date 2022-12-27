import sys
import logging
from typing import List
import asyncio
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
from aiohttp_socks import ProxyConnector # Проксей не будет 
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


url: str = "https://parsinger.ru/html/index1_page_1.html"
head_url: str = "/".join(url.split("/")[:-1]) + "/"


async def get_soup(_url: str, _session: aiohttp.ClientSession) -> BeautifulSoup:
    client_session = _session
    retry_client = RetryClient(client_session=client_session, exponential_retry=ExponentialRetry(attempts=5))
    async with retry_client.get(_url) as response:
        return BeautifulSoup(await response.text(), "lxml")
            

async def get_nav_menu(_url: str, _head_url: str, _session: aiohttp.ClientSession) -> List[str]:
    soup = await get_soup(_url, _session)
    logger.debug(f"{_url} ok")
    return [_head_url + nav["href"] for nav in soup.find("div", class_="nav_menu").find_all("a")]
    

async def get_pagens(_nav_link: str, _head_url: str, _session: aiohttp.ClientSession) -> List[str]:
    soup = await get_soup(_nav_link, _session)
    logger.debug(f"{_nav_link} ok")
    return [_head_url + pgn["href"] for pgn in soup.find("div", class_="pagen").find_all("a")]


async def get_urls(_all_item_urls: str, _head_url: str, _session: aiohttp.ClientSession) -> List[str]:
    soup = await get_soup(_all_item_urls, _session)
    logger.debug(f"{_all_item_urls} ok")
    return [_head_url + url["href"] for url in soup.find("div", class_="item_card").find_all("a", class_="name_item")]


async def get_price(_item_url: str, _session: aiohttp.ClientSession) -> int:
    soup = await get_soup(_item_url, _session)
    price = soup.find("span", id="price").text.split(" ")[0] 
    old_price = soup.find("span", id="old_price").text.split(" ")[0]
    stock = soup.find("span", id="in_stock").text.split(": ")[-1]
    result = (int(old_price) - int(price)) * int(stock)
    logger.debug(f"{_item_url} ok")
    return result    


async def main(_url: str, _head_url: str) -> None:
    fake_user_agent = {"user-agent": UserAgent().random}
    async with aiohttp.ClientSession(headers=fake_user_agent) as session:
        nav_menu = await get_nav_menu(_url, _head_url, session)
        task_for_getpagens = [get_pagens(nav_link, head_url, session) for nav_link in nav_menu]
        result_getpagens = await asyncio.gather(*task_for_getpagens)

        list_task_forget_allurls = []
        for nav in result_getpagens:
            list_task_forget_allurls.extend(nav)
        task_forget_allitems_url = [get_urls(all_items_url, head_url, session) for all_items_url in list_task_forget_allurls]
        result_get_urls = await asyncio.gather(*task_forget_allitems_url)

        list_task_foget_price = []
        for urls in result_get_urls:
            list_task_foget_price.extend(urls)
        task_forget_price = [get_price(item_url, session) for item_url in list_task_foget_price]
        result_forget_price = await asyncio.gather(*task_forget_price)
        print(f"result: {sum(result_forget_price)}")

        

if __name__ == "__main__":
    # logging
    logger = logging.getLogger(__file__.split("/")[-1])
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(name)s, %(funcName)s, %(levelname)s, %(asctime)s, %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG) # after debug set to logging.WARNING
    #
    asyncio.run(main(url, head_url))

    logger.debug("Done")