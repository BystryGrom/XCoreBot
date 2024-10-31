import mysql.connector
from mysql.connector import connect
from bot import SETTINGS

#
#     БЕГИТЕ Я КОНЧЕННЫЙ
#     НАГОВНОКОДИЛ ПО МАКСИМУМУ
#

class DB:

    @staticmethod
    def _open_connection() -> connect():
        try:
            connection = connect(host=SETTINGS["db_host"],
                                 database=SETTINGS["db_name"],
                                 user=SETTINGS["db_user"],
                                 password=SETTINGS["db_password"])
            return connection
        except Exception as e:
            print(e)

    def select(self, table: str, coloumn: str = "*", condition: str = "") -> list:
        connection = self._open_connection()
        query = f"""SELECT {coloumn} FROM {table}{f'{" " + condition}' if condition != "" else condition}"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        connection.close()
        return result

    def insert(self, table: str, coloumns: list[str], datas: list[tuple]):
        connection = self._open_connection()
        query = f"""INSERT INTO {table} ({f'{coloumns}'[1:-1].replace("'", '')}) VALUES ({'%s' + ', %s' * (len(coloumns) - 1)})"""
        with connection.cursor() as cursor:
            cursor.executemany(query, datas)
            connection.commit()
        connection.close()

    def update(self, table: str, update_data: str, condition: str):  # Похуй, у нас не бывает апдейта без условия
        connection = self._open_connection()
        query = f"""UPDATE {table} SET {update_data} WHERE {condition}"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
        connection.close()

    def delete(self, table: str, condition: str):
        connection = self._open_connection()
        query = f"""DELETE FROM {table} WHERE {condition}"""
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
        connection.close()


DbWork = DB()
