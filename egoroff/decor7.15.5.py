from functools import wraps

def double_it(func):

    @wraps(func)
    def double(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return double


@double_it
def multiply(num1, num2):
    """DCOCDCDC"""
    return num1 * num2

res = multiply(9, 4) # произведение 9*4=36, но декоратор double_it удваивает это значение
print(res)

sqr = double_it(multiply)
print(sqr.__name__)
print(sqr.__doc__)

# from functools import wraps
# def table(func):

#     @wraps(func)
#     def inner(*args, **kwargs):
#         print('<table>')
#         func(*args, **kwargs)
#         print('</table>')
#     return inner

# def sqr(x):
#     '''
#     Функция возводит в квадрат
#     :param x:
#     :return:
#     '''
#     print(x**2)

# sqr = table(sqr)
# print(sqr)
# print(sqr.__name__)
# help(sqr)