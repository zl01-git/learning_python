from logger import logger

@logger
def some_func(word):
    for letter in word:
        print(letter)


some_func("blablalasddqwdqfqf")
some_func("again")