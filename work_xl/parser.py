import time

import requests as rq
import bs4
import fake_useragent

ua = fake_useragent.UserAgent()

headers = {
    "user-agent": ua.random
}

main_link = "https://knkamur.ru"


def parse_link_categories(main_link):

    # Отправляется запрос по ссылке
    req = rq.get(main_link, headers=headers)

    # Открывается файл index.html для записи html кода
    with open("index.html", "r", encoding="utf-8") as file:
         info = file.read()

    # Преобразуем этот код для работы с ним
    soup = bs4.BeautifulSoup(info, "lxml")

    # Ищем контейнер в котором находятся ссылки
    pre_link = soup.find_all("div", class_="catalog-section-list-tile-img-container embed-responsive embed-responsive-16by9")

    # Записываются данные в файл categories.txt
    with open("link/categories.txt", "w", encoding="utf-8") as file:
        for i in pre_link:
            link = main_link + i.find("a")["href"]
            file.writelines(link + "\n")


def parse_link_product(link):

    # Отправляем запрос по ссылке
    req = rq.get(link, headers=headers)

    # Преобразуем полученный html код
    soup = bs4.BeautifulSoup(req.text, "lxml")

    # Получаем контейнер с информацией о названии и цене товара
    info_box = soup.find_all("div", class_='product_item_name_box')

    # Открываем файл в который будем записывать данные
    with open("file_data.txt", "a", encoding="utf-8") as file_w:
        # Получаем и записываем названия и цены товаров
        for i in info_box:
            file_w.write(i.find("span").text + "\t")
            file_w.write(i.find("a")["title"] + "\n")

    # Возвращаем общее количество страниц в категории
    return soup.find("ul", class_="bx_pagination_page_list_num").find_all("li")[-1].text


def main():

    # parse_link_categories(main_link)  # запускается для начального получения ссылок

    # Открываем файл для, чтение ссылок
    with open("link/categories.txt", "r", encoding="utf-8") as file:
        link = file.readlines()

    # Проходимся по ссылкам взятым из файла
    for i in link:
        j = 1
        while True:
            # Убирая знак перехода на новую строку и добавляя № страницы каталога
            sub_link = i.replace("\n", "") + f"?PAGEN_2={j}&SIZEN_2=21"

            # Записываем результат работы функции
            max_val = parse_link_product(sub_link)

            # Прибавляем 1 к номеру каталога
            j += 1

            # Останавливаем работу цикла если j больше чем количество страниц в категории
            if j > int(max_val):
                break

            # На всякий случай делаем паузу в 3 секунды
            time.sleep(3)

            # Выводим что-то чтобы, понять что парсер работает и не смотреть в пустой терминал
            print(j)


main()