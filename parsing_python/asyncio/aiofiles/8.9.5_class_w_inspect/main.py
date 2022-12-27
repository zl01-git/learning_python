import loggit  # comment it to debug OFF
from program import ParsingImages


if __name__ == "__main__":
    print(f"Getting images size, please wait a minute ...")
    url = "https://parsinger.ru/asyncio/aiofile/2/index.html"
    path_name = "saved_images"
    images = ParsingImages(url, path_name)
    size = images()
    print(f"Images size = {size}")