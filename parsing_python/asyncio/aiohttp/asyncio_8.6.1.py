import asyncio
import aiohttp


async def first(message) -> None:
    print("start first")
    await asyncio.sleep(2)
    print(message)


async def second(message) -> None:
    print("start second")
    await asyncio.sleep(0.5)
    print(message)



async def main():
    task1 = first("first message")
    task2 = second("second message")
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    asyncio.run(main())