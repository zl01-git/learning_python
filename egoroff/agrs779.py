
def check_sum(*args) -> None:
    if sum(args) < 50:
        print("not enough")
    else:
        print("verification passed")


numbers = list(map(int, input().split()))
check_sum(*numbers)