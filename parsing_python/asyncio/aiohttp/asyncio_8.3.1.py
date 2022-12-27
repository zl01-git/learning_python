import asyncio
import aiohttp
from codetiming import Timer

urls = ["http://google.com",
        "http://yahoo.com",
        "http://apple.com",
        "http://microsoft.com",
        "https://habr.com/",
        "https://www.youtube.com/",
        "https://stepik.org/",
        "https://docs.python.org/",
        "https://stackoverflow.com/",
        "https://www.reg.ru/"]


async def main(url):
    with Timer(text=f"Elapsed time: {{:0.4f}} seconds"):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                print(response.url)


if __name__ == "__main__":
    tasks = [main(url) for url in urls]
    asyncio.run(asyncio.wait(tasks))
