import os
import shutil
import numpy
from typing import List
import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup


class ParsingImages:
    def __init__(self, url: str, dir: str) -> None:
        self._url = url
        self._root = "/".join(self._url.split("/")[:-1]) + "/"
        self._root_depth2 = ""
        self._dir_name = dir
        self._size = 0
        self._check_dir()


    def _check_dir(self):
        if os.path.exists(self._dir_name):
            shutil.rmtree(self._dir_name)
        os.mkdir(self._dir_name)


    async def _get_soup(self, url: str, session: aiohttp.ClientSession) -> BeautifulSoup:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.text(), "lxml")
            return soup


    def _make_category_depth1(self, soup: BeautifulSoup) -> List[str]:
        category = soup.find_all("a", class_="lnk_img")
        cat_lnk = [self._root + lnk["href"] for lnk in category]
        self._root_depth2 = "/".join(cat_lnk[0].split("/")[:-1]) + "/"
        return cat_lnk

    
    def _make_category_depth2(self, soup: BeautifulSoup) -> List[str]:
        category = soup.find_all("a", class_="lnk_img")
        cat_lnk = [self._root_depth2 + lnk["href"] for lnk in category]
        return cat_lnk

    
    def _make_img_urls(self, soups: List[BeautifulSoup]) -> List[str]:
        img_urls = []
        for soup in soups:
            items = soup.find_all("img", class_="picture")
            for item in items:
                img_urls.append(item["src"])
        return img_urls


    async def _save_images(self, url: str, session: aiohttp.ClientSession) -> None:
        file_name = url.split("/")[-1]
        async with aiofiles.open(f"{self._dir_name}/{file_name}", "wb") as file:
            async with session.get(url) as response:
                async for piece in response.content.iter_chunked(1024):
                    await file.write(piece)


    def _get_size(self):
        for root, _, files in os.walk(self._dir_name):
            for file in files:
                self._size += os.path.getsize(os.path.join(root, file))


    async def _main(self):
        async with aiohttp.ClientSession() as session:
            soup = await self._get_soup(self._url, session)
            category_depth1 = self._make_category_depth1(soup)
            
            task = [self._get_soup(lnk, session) for lnk in category_depth1]
            soup_category_depth2 = await asyncio.gather(*task)
            category_depth2 = [self._make_category_depth2(cat) for cat in soup_category_depth2]
            
            task2 = []
            for cat in category_depth2:
                for lnk in cat:
                    task2.append(self._get_soup(lnk, session))
            splits = numpy.array_split(task2, 100)
            soup_img_urls = []
            for _task in splits:
                soup_img_urls.extend(await asyncio.gather(*_task))

            img_urls = self._make_img_urls(soup_img_urls)
            full_task = [self._save_images(img, session) for img in img_urls]
            splits = numpy.array_split(full_task, 1000)
            for _task in splits:
                await asyncio.wait_for(*_task)

            self._get_size()


    def __call__(self) -> int:
        asyncio.run(self._main())
        return self._size


