from program import ParsingImages
import logit
import time


if __name__ == "__main__":
    start = time.time() 
    url = "https://parsinger.ru/asyncio/aiofile/3/index.html"
    dir_name = "saved_images"
    getimg = ParsingImages(url, dir_name)
    size = getimg()
    print(size)
    print(time.time() - start)