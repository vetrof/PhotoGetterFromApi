import time

import requests
from jsonpath_ng import jsonpath, parse


def save_photo(link, new_filename):
    for _ in range(10):
        try:
            resp = requests.get(link)
            if resp.status_code == 200:
                with open(f"image/{new_filename}", 'wb') as f:
                    f.write(resp.content)
                print('all ok --> ', new_filename)
                return
            else:
                print(resp.status_code)
                time.sleep(5)
                continue

        except Exception as e:
            print('Error:', e)
            time.sleep(10)
            continue

    print('ERROR', new_filename)
    with open(f"image/bad_links.txt", 'a') as f:
        f.write(link + '\n')


def get_category(url):
    res = requests.get(url)
    jsonpath_expr = parse('$..categories..id')
    matches = [match.value for match in jsonpath_expr.find(res.json())]
    return sorted(set(matches))


def get_photo_link(prefix_url, cat_list):
    count = 0
    for cat in cat_list:
        url = prefix_url + str(cat)

        while url:
            try:
                response = requests.get(url)
                data = response.json()
                goods_info = data.get('results')

                for good_info in goods_info:
                    for image in good_info['photos']:
                        id_product = good_info['id']
                        link = image['image']
                        id_image = image['id']
                        new_filename = f'{id_image}-{id_product}'
                        count += 1
                        print(count, id_image, new_filename, link)
                        save_photo(link, new_filename)

                url = data.get('next')
            except Exception as e:
                print('Error: get_photo_link ------------>>> ', e)
