import sqlite3 as sq

def sql_start():
    global base, cur
    base = sq.connect("datab.db")
    cur = base.cursor()
    if base:
        print("Database is OK")

    #База
    base.execute("""CREATE TABLE IF NOT EXISTS users (
        login TEXT, 
        password TEXT,
        cash BIGINT
    )""") #BIGINT - Тип данных означающее число. От 0 до Сикстилионов

    base.commit() #Подтверждение действия (Создание таблицы)


    user_login = input("Login: ")
    user_password = input("Password: ")

    base.execute("SELECT login FROM users") #SELECT - выбрать "login", так же с помощью * можно выбрать все; FROM - в столбце "users"
    if base.fetchone() is None:
        base.execute("INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
        base.commit()

        print("Зарегистрировано!")
    else:
        print("Такая запись уже имеется")