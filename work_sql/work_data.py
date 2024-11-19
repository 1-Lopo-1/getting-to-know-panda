import pandas as pd
import json
from work_db import DB

db = DB()

with open("main.json", "r", encoding="utf-8") as file:
    # Вытаскиваем все данные из json файла
    info = json.load(file)

"""
Создание словаря с двумя ключами в которых находятся словари
Для преобразования данных в удобный формат
С последующей передачей данных в метод pandas
"""
dict_name_and_price = {"name": [], 'price': []}

# Проход по всем данным из json
for i in info:
    # Вытаскиваем из основного словаря все словари содержащие имена и цену
    for j in i['items']:
        # Запись данных в списки внутри словарей
        dict_name_and_price["name"].append(j["name"])
        dict_name_and_price["price"].append(j["price"])

# Преобразование данных в таблицу
data_frame = pd.DataFrame(dict_name_and_price)

# name название таблицы в БД con подключение к БД if_exists действия если столбец существует
data_frame.to_sql(name="product", con=db.con, if_exists="replace", index=True)

# Достаёт все данные из базы данных обратно
data_db = pd.read_sql(sql="select * from product", con=db.con, index_col='index')

# Вывод всех данных из таблицы product
print(data_db)

db.close_con()