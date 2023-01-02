import os
import time
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
        self._check_dir()
        self._size = 0


    def _check_dir(self):
        if os.path.exists(self._dir_name):
            shutil.rmtree(self._dir_name)
        os.mkdir(self._dir_name)


    async def _get_soup(self, url: str,
                              session: aiohttp.ClientSession) -> BeautifulSoup:
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


    async def _save_images(self, url: str, 
                                       session: aiohttp.ClientSession) -> None:
        file_name = url.split("/")[-1]
        async with aiofiles.open(f"{self._dir_name}/{file_name}", "wb") as fl:
            async with session.get(url) as response:
                async for piece in response.content.iter_chunked(1024*1024):
                    await fl.write(piece)


    def _get_size(self):
        for root, _, files in os.walk(self._dir_name):
            for file in files:
                self._size += os.path.getsize(os.path.join(root, file))


    async def _main(self):
        async with aiohttp.ClientSession() as session:
            soup = await self._get_soup(self._url, session)
            cat_depth1 = self._make_category_depth1(soup)
            
            task = [asyncio.create_task(self._get_soup(lnk, session))
                                                         for lnk in cat_depth1]
            soup_cat_depth2 = await asyncio.gather(*task)

            cat_depth2 = [self._make_category_depth2(cat)
                                                    for cat in soup_cat_depth2]
            for cat in range(len(cat_depth2)):
                for lnk in range(len(cat_depth2[cat])):
                    cat_depth2[cat][lnk] = asyncio.create_task(
                                 self._get_soup(cat_depth2[cat][lnk], session))
            
            soup_img_urls = []
            for _task in cat_depth2:
                soup_img_urls.extend(await asyncio.gather(*_task))

            img_urls = list(set(self._make_img_urls(soup_img_urls)))
            full_task = [asyncio.create_task(self._save_images(img, session))
                                                           for img in img_urls]
            splits = numpy.array_split(full_task, 1000)
            for _task in splits:
                await asyncio.gather(*_task)

            self._get_size()


    def __call__(self) -> int:
        asyncio.run(self._main())
        return self._size


if __name__ == "__main__":
    print("Please wait... ~ 200 seconds")
    start = time.time() 
    url = "https://parsinger.ru/asyncio/aiofile/3/index.html"
    dir_name = "saved_images"
    getimg = ParsingImages(url, dir_name)
    size = getimg()
    print(f"Size downloaded images = {size}")
    print(f"Finished at {round(time.time() - start, 2)} seconds")