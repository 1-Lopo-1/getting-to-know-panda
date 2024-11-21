import pandas as pd
import xlsxwriter

list_price = {"price": []}
list_product_name = {"name": []}

# Вытаскиваю данные из файла
with open("file_data.txt", "r", encoding="utf-8") as df:
    for i in df.readlines():
        i_spl = i.split("₽")
        list_price["price"].append(i_spl[0] + "₽")
        list_product_name["name"].append(i_spl[-1].replace("\n", "").replace("\t", ""))

# Создаём DataFrames
df_price = pd.DataFrame(list_price)

df_name = pd.DataFrame(list_product_name)

# Добавляем к первому frama второго
ful_data_frame = df_name.join(df_price)

# Не работает когда уже запущен xl файл
with pd.ExcelWriter("myFile.xlsx", engine="xlsxwriter", mode="w") as writer:
    ful_data_frame.to_excel(writer, index=False, sheet_name="infoList")