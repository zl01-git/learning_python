

def text_decor(func):
    def inner(*args):
        print("Hello")
        func()
        print("Goodbye")
    return inner


@text_decor
def somefunc():
    print("some_func")


somefunc()
