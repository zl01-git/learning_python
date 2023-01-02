from program import ParsingImages
import logit


if __name__ == "__main__":
    print("start_program.py")
    url = "https://parsinger.ru/asyncio/aiofile/3/index.html"
    dir_name = "saved_images"
    getimg = ParsingImages(url, dir_name)
    size = getimg()
    print("finish_program.py")
    print(size)