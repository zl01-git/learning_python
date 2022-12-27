import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://parsinger.ru/html/index1_page_1.html") as response:
            # print(await response.text())
            print(response.request_info)


if __name__ == "__main__":
    asyncio.run(main())