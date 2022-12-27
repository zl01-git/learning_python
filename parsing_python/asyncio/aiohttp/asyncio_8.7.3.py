import asyncio
import aiohttp

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}
url = 'http://httpbin.org/get'
data = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}


async def main(_url, _headers, _data):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=_url, headers=_headers, data=_data) as response:
            print(await response.text())


if __name__ == "__main__":
    asyncio.run(main(url, headers, data))