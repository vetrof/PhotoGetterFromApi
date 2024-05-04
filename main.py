import os
from dotenv import load_dotenv
from utils import get_photo_link, get_category

load_dotenv()

category_url = os.getenv('category_url')
goods_url = os.getenv('goods_url')


def main():
    category_list = get_category(category_url)
    image_link_list = get_photo_link(goods_url, category_list)


if __name__ == '__main__':
    main()