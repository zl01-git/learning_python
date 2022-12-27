import sys
from time import time
import logging
from typing import List, Tuple
import asyncio
import aiohttp
from aiohttp_retry import RetryClient, ExponentialRetry
from bs4 import BeautifulSoup


url = "https://parsinger.ru/asyncio/create_soup/1/index.html"
head_url = "/".join(url.split("/")[:-1]) + "/"
result_list = []


async def get_soup(_url: str, _session: aiohttp.ClientSession) -> Tuple[BeautifulSoup, bool]:
    client_session = _session
    retry_client = RetryClient(client_session=client_session, exponential_retry=ExponentialRetry(attempts=5))
    async with retry_client.get(_url) as response:
        logger.debug(f"status: {response.status}")
        return BeautifulSoup(await response.text(), "lxml"), response.ok


async def get_urls(_url: str, _head_url: str, _session: aiohttp.ClientSession) -> List[str]:
    soup, _ = await get_soup(_url, _session)
    return [_head_url + url["href"] for url in soup.find("div", class_="item_card").find_all("a", class_="lnk_img")]
    

async def get_result(_url: str, _session: aiohttp.ClientSession) -> None:
    soup, status = await get_soup(_url, _session)
    if status:
        number = soup.find("p", class_="text").text
        result_list.append(number)


async def main(_url: str, _head_url: str) -> None:
    async with aiohttp.ClientSession() as session:
        urls = await get_urls(_url, _head_url, session)
        task = [get_result(url, session) for url in urls]
        await asyncio.gather(*task)
        print(f"result: {sum(map(int, result_list))}")
    

if __name__ == "__main__":
    start = time()
    ### logging
    logger = logging.getLogger(__file__.split("/")[-1])
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(name)s, %(funcName)s, %(levelname)s, %(asctime)s, %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO) # logging.DEBUG
    ###
    logger.info(f"The parser is starting, please wait a few seconds")
    asyncio.run(main(url, head_url))
    logger.info(f"Completed at {time() - start} seconds")