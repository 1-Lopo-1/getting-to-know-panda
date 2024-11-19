import sqlite3


class DB:

    def __init__(self):
        self.con = sqlite3.connect("Название бд или путь до неё")
        self.cur = self.con.cursor()

    # Открытие связи с БД если мы её закрыли
    def open_con(self):
        try:
            self.con = sqlite3.connect("Название бд или путь до неё")
            self.cur = self.con.cursor()
        except Exception as ex:
            print(ex)

    # Закрытие связи с БД
    def close_con(self):
        try:
            self.cur.close()
            self.con.close()
        except Exception as ex:
            print(ex)

    def select_all_data_product(self):
        return self.cur.execute("""select * from product""").fetchall()