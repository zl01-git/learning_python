import asyncio
import aiohttp
from bs4 import BeautifulSoup


url = "https://parsinger.ru/html/index1_page_1.html"


async def get_soup(_url: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=_url, timeout=1) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            name = soup.find_all("a", class_="name_item")
            price = soup.find_all("p", class_="price")
    for nm, pr in zip(name, price):
        print(nm.text, pr.text)


if __name__ == "__main__":
    asyncio.run(get_soup(url))