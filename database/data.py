import sqlite3

# Создание соединения с базой данных
db = sqlite3.connect('server.db')
sql = db.cursor() #Курсор нужен для работы с баззой данных - удаление и добавление

#База
sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT, 
    password TEXT,
    cash BIGINT
)""") #BIGINT - Тип данных означающее число. От 0 до Сикстилионов

db.commit() #Подтверждение действия (Создание таблицы)


user_login = input("Login: ")
user_password = input("Password: ")

sql.execute("SELECT login FROM users") #SELECT - выбрать "login", так же с помощью * можно выбрать все; FROM - в столбце "users"
if sql.fetchone() is None:
    sql.execute("INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
    db.commit()

    print("Зарегистрировано!")
else:
    print("Такая запись уже имеется")