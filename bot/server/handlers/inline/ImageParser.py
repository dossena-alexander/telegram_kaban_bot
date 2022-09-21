from dataclasses import dataclass
import requests
import json
from fake_headers import Headers
from bs4 import BeautifulSoup as bs4


@dataclass
class _Size():
    large: str = 'large'
    medium: str = 'medium'
    small: str = 'small'


class _Preview:
    def __init__(self, url: str,
                 width: int,
                 height: int):
        self.url = url
        self.width = width
        self.height = height
        self.size = str(width) + '*' + str(height)


class _Result:
    def __init__(self, title: str | None,
                 description: str | None,
                 domain: str,
                 url: str,
                 width: int,
                 height: int,
                 preview: _Preview):
        self.title = title
        self.description = description
        self.domain = domain
        self.url = url
        self.width = width
        self.height = height
        self.size = str(width) + '*' + str(height)
        self.preview = preview


class YandexImage:
    def __init__(self):
        self.headers = Headers(headers=True).generate()

    def search(self, query: str, size: str = _Size.large) -> list[_Result]:
        request = requests.get('https://yandex.ru/images/search',
                               params={"text": query,
                                       "nomisspell": 1,
                                       "noreask": 1,
                                       "isize": size
                                       },
                               headers=self.headers)

        soup = bs4(request.text, 'html.parser')
        items_place = soup.find('div', {"class": "serp-list"})
        output = []
        try:
            items = items_place.find_all("div", {"class": "serp-item"})
        except AttributeError:
            return output

        for item in items:
            data = json.loads(item.get("data-bem"))
            image = data['serp-item']['img_href']
            image_width = data['serp-item']['preview'][0]['w']
            image_height = data['serp-item']['preview'][0]['h']

            snippet = data['serp-item']['snippet']
            try:
                title = snippet['title']
            except KeyError:
                title = None
            try:
                description = snippet['text']
            except KeyError:
                description = None
            domain = snippet['domain']

            preview = 'https:' + data['serp-item']['thumb']['url']
            preview_width = data['serp-item']['thumb']['size']['width']
            preview_height = data['serp-item']['thumb']['size']['height']

            output.append(_Result(title, description, domain, image,
                                 image_width, image_height,
                                 _Preview(preview, preview_width, preview_height)))

        return output

    def gen_search(self, query: str, sizes: _Size = 'large') -> _Result:
        request = requests.get('https://yandex.ru/images/search',
                               params={"text": query,
                                       "nomisspell": 1,
                                       "noreask": 1,
                                       "isize": sizes
                                       },
                               headers=self.headers)

        soup = bs4(request.text, 'html.parser')
        items_place = soup.find('div', {"class": "serp-list"})
        try:
            items = items_place.find_all("div", {"class": "serp-item"})
        except AttributeError:
            return ''

        for item in items:
            data = json.loads(item.get("data-bem"))
            image = data['serp-item']['img_href']
            image_width = data['serp-item']['preview'][0]['w']
            image_height = data['serp-item']['preview'][0]['h']

            snippet = data['serp-item']['snippet']
            try:
                title = snippet['title']
            except KeyError:
                title = None
            try:
                description = snippet['text']
            except KeyError:
                description = None
            domain = snippet['domain']

            preview = 'https:' + data['serp-item']['thumb']['url']
            preview_width = data['serp-item']['thumb']['size']['width']
            preview_height = data['serp-item']['thumb']['size']['height']

            yield _Result(title, description, domain, image,
                                 image_width, image_height,
                                 _Preview(preview, preview_width, preview_height))
