import sqlite3

data_base = sqlite3.connect('datab.db') # путь к базе данных
cursor = data_base.cursor()


data_base.commit() # завершение работы
