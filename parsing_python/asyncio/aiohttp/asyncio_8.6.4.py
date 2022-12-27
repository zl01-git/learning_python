import asyncio
import random


async def first(x):
    print("first_start")
    await asyncio.sleep(random.randint(1, 5))
    await second(x)
    return print(x, "first_finish")


async def second(x):
    print("second_start")
    await asyncio.sleep(random.randint(2,4))
    print(x, "second_finish")


async def main():
    print("start_main")
    lst = [x for x in range(10)]
    tasks_lst = []
    for x in lst:
        task = asyncio.create_task(first(x), name="first")
        tasks_lst.append(task)
    await asyncio.gather(*tasks_lst)
    print("stop_main")

if __name__ == "__main__":
    asyncio.run(main())