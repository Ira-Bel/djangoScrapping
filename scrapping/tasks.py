from bs4 import BeautifulSoup
import requests
from time import sleep
from random import choice

from celery import shared_task

from .models import Goods


desktop_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
]


def random_headers():
    return {
        "User-Agent": choice(desktop_agents),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }


@shared_task
def parse_page():
    list_items = []
    for count in range(1, 2):  # change range(1, 89)
        print("start")
        sleep(1)
        url = f"https://skinfood.by/catalog/litso/filter/strana-is-1d7e7a19-533c-11ea-80c0-00155d0a0360/apply/?PAGEN_4={count}"
        response = requests.get(url, headers=random_headers())
        soup = BeautifulSoup(response.text, "lxml")
        data = soup.find_all("div", class_="product")
        for item in data:
            name = item.find("span", class_="product__title").text
            image_link = "https://skinfood.by" + item.find(
                "img", class_="product__image"
            ).get("src")
            description = item.find("span", class_="product__subtitle").text
            price = float(
                item.find("span", class_="product__price").text.replace("BYN", "")
            )
            item = {
                "name": name,
                "image_link": image_link,
                "description": description,
                "price": price
            }
            list_items.append(item)
        print("end")
        return save(list_items)


@shared_task(serializer='json')
def save(list_items):
    count = 0
    for item in list_items:
        Goods.objects.create(
            name=item["name"],
            image_link=item["image_link"],
            description=item["description"],
            price=item["price"]
        )
        count += 1
    return print("done")
