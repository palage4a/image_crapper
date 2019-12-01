import os
import time
import requests
import json
from bs4 import BeautifulSoup
from functools import reduce

class Utils:
    header = {
            'User-Agent' :
                'Mozilla/5.0 (X11; Linux x86_64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/78.0.3904.108 Safari/537.36'
            }
    @staticmethod
    def get_soup_page(url):
        res = requests.get(url, headers = Utils.header)
        if res.status_code == 200:
            return BeautifulSoup(res.text, 'html.parser')
        else:
            return res.status_code

    @staticmethod
    def extract_image_src(soup):
        div_with_img = soup.find(id="mmComponent_images_1")
        li_with_img = div_with_img.find_all('li')
        links = [ img.find('a') for img in li_with_img ]
        json_with_src = [ link['m'] for link in links ]
        srcs = [ eval(json)['turl'] for json in json_with_src ]
        return srcs

    @staticmethod
    def download_images(links, dataset):
        def download_count(acc, link):
            if os.path.isdir('outputs'):
                pass
            else:
                os.mkdir('outputs')
            with open(f"outputs/{ dataset }_{acc}", 'wb') as f:
                try:
                    img = requests.get(link, headers=Utils.header)
                except requests.exceptions.ConnectionError as error:
                    print(f"\r\n!!!! - Catch error:\n\
                    \r{repr(error)}\n\
                    \rOn link: {link}\n\
                    \rImage not found on this link")
                    return acc
                f.write(img.content)
            return acc + 1
        return reduce(download_count, links, 0)

