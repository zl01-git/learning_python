import os
import shutil
from typing import List
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup


class ParsingImages:
    def __init__(self, url: str, path_name: str):
        self.url = url
        self._main_url = "/".join(url.split("/")[:-1]) + "/"
        self._files_size = 0
        self._path_name = path_name
        if os.path.exists(self._path_name):
            shutil.rmtree(self._path_name)
        os.mkdir(self._path_name)


    async def get_soup(self, _url: str, 
                _session: aiohttp.ClientSession) -> BeautifulSoup:
        async with _session.get(_url) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            return soup


    def _make_pagen_urls(self, _soup: BeautifulSoup) -> List[str]:
        item_card = _soup.find("div", class_="item_card")
        raw_lnk = item_card.find_all("a", class_="lnk_img") # type: ignore
        pagens = [self._main_url + lnk["href"] for lnk in raw_lnk]
        return pagens


    def _make_img_urls(self, img_soups: List[BeautifulSoup]) -> List[str]:
        lst = []
        for img_soup in img_soups:
            img_urls = img_soup.find_all("img", class_="picture")
            for img_url in img_urls:
                lst.append(img_url["src"])
        return lst


    async def _get_img(self, _session: aiohttp.ClientSession, \
                                                    _url: str) -> None:
        file_name = _url.split("/")[-1]
        async with aiofiles.open(f"{self._path_name}/{file_name}", \
                                                    mode="wb") as file:
            async with _session.get(_url) as response:
                async for piece in response.content.iter_chunked(1024):
                    await file.write(piece)

    
    def _get_files_size(self, path) -> None:
        for root, _, files in os.walk(path):
            for file in files:
                self._files_size += os.path.getsize(os.path.join(root, file))
        

    async def _main(self) -> None:
        async with aiohttp.ClientSession() as session:
            pagen_soup = await self.get_soup(self.url, session)
            pagens = self._make_pagen_urls(pagen_soup)

            soups_task = [self.get_soup(page, session) for page in pagens]
            img_soups = await asyncio.gather(*soups_task)

            img_urls = self._make_img_urls(img_soups)

            downloads_task = [self._get_img(session, url) for url in img_urls]
            await asyncio.gather(*downloads_task)
            
            self._get_files_size(self._path_name)


    def __call__(self) -> float:
        asyncio.run(self._main())
        return self._files_size


if __name__ == "__main__":
    print(f"Getting images size, please wait a minute ...")
    url = "https://parsinger.ru/asyncio/aiofile/2/index.html"
    path_name = "saved_images"
    images = ParsingImages(url, path_name)
    size = images()
    print(f"Images size = {size}")