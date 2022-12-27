import asyncio
from random import randint
from logger import log, async_log


class Message:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


    @log
    def is_adult(self) -> bool:
        if self.age > 17: 
            return True
        return False


    @log
    def say_hello(self) -> str:
        return f"Hello {self.name}"


if __name__ == "__main__":
    user_list = []
    
    for id in range(10):
        user = Message(f"name{id}", randint(12, 30))
        user_list.append(user)

    for user in user_list:
        print(user.is_adult())
        print(user.say_hello())