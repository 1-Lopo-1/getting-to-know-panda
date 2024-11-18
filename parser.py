import time
import json

import requests as rq
import bs4
from fake_useragent import UserAgent


def data_from_url(url):
    # Создание словаря для записи данных в json
    data = {"items": []}

    # Отправка get запроса по url
    _url = rq.get(url, headers=headers)

    # Получение возможности забирать из html кода данные
    soup = bs4.BeautifulSoup(_url.text, "lxml")

    # Получение основного контейнера в котором находиться все контейнеры с информацией о продуктах
    product_div1 = soup.find("div", class_="row row-cols-2 row-cols-md-3 row-cols-lg-4 row-cols-xxl-5")

    # Сбор всех контейнеров в которых находятся данные о цене и названии продукта
    if product_div1 is not None:
        product_div = product_div1.find_all("div", class_="col")

        for i in product_div:
            # Указание где, находятся данные более конкретно
            sub_div = i.find("div", class_="product-item__info")

            if sub_div is None:
                continue
            else:
                # Сбор названия товара и его цены
                text = sub_div.find_all("span")
                sub_dict = {}
                sub_list = ["name", "price"]
                k = 0

                for j in text:
                    sub_dict[sub_list[k]] = j.text.strip()
                    k += 1

                # Запись данных в словарь
                data["items"].append(sub_dict)
        """
        Производим запись в json файл (работает, чутка кривовато стоит 
        подправить, то как ставить запятые и положить это всё в список)
        """
        with open("main.json", 'a', encoding="UTF-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            json.dump(',', file, ensure_ascii=False, indent=4)


ua = UserAgent()

headers = {
     "user-agent": ua.random
}

"""
Данные для начального парсинга ссылок для дальнейшей работы над ними

url = "https://snab28.ru"

r = rq.get(url, headers=headers)

with open("index.html", "w", encoding='utf-8') as file:
    file.write(r.text)

with open("index.html", "r", encoding='utf-8') as file:
    src = file.read()

soup = bs4.BeautifulSoup(src, "lxml")

cataloged = soup.find("div", class_="standart-catalog")

load_tipe = cataloged.find("ul", {"class": "sidebar-menu__wrapper"})

links_to_categories = load_tipe.find_all("a", class_="sidebar-menu__link has-children sidebar-menu__link_hover_green")

sub_categories_link = load_tipe.find_all("a", class_="sidebar-menu__link sidebar-menu__link_hover_text_green")

for i in sub_container:
    print(i["href"])

with open("link/link_to_sub_categories", 'w', encoding='utf-8') as file:
    for i in sub_categories_link:
        file.writelines(url+i["href"]+"\n")
"""

# Принимает ссылки и выполняет функцию
with open("link/link_to_sub_categories", 'r', encoding="utf-8") as file:
    list_of_url = file.readlines()
    for i in list_of_url:
        url = i.replace("\n", '')
        data_from_url(url)
        time.sleep(5)