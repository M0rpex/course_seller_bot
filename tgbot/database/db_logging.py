import sqlite3
from tgbot.data.config import PATH_DATABASE
from openpyxl import Workbook



#############################################  ВЗАИМОДЕЙСТВИЕ С storage_users  #################################################
################################################################################################################################


def add_userx(reg_date, user_id, user_login, user_name, alarm_time):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_users "
                    "(reg_date, user_id, user_login, user_name, alarm_time) "
                    "VALUES (?, ?, ?, ?, ?)",
                    [reg_date, user_id, user_login, user_name, alarm_time])
        con.commit()


def get_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


def update_userx(user_id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_users SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(user_id)
        con.execute(sql + "WHERE user_id = ?", parameters)
        con.commit()


def get_all_userx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


def get_all_users_user_idx():
    conn = sqlite3.connect(PATH_DATABASE)  # Подставьте имя вашей базы данных SQLite
    cursor = conn.cursor()

    # Запрашиваем пользователей, у которых значение столбца evry_day равно 1
    cursor.execute("SELECT user_id FROM storage_users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users


def get_all_userx_where(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_users"
        sql, parameters = update_format_where(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


#############################################  ВЗАИМОДЕЙСТВИЕ С bot_settings  ##################################################
################################################################################################################################


def get_advicexx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_advice"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


def get_settingsx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM bot_settings"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


def get_settings_allx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM bot_settings"
        return con.execute(sql).fetchall()



def add_transx(user_id, user_name, order_date):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_transaction"
                    "(user_id, user_name, order_date) "
                    "VALUES (?, ?, ?)",
                    [user_id, user_name, order_date])
        con.commit()



def add_questx(user_id, user_name, text, status, date):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        con.execute("INSERT INTO storage_support"
                    "(user_id, user_name, text, status, date) "
                    "VALUES (?, ?, ?, ?, ?)",
                    [user_id, user_name, text, status, date])
        con.commit()


def get_req_allx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_support"
        sql, parameters = update_format_where(sql, kwargs)
        return con.execute(sql, parameters).fetchall()


def get_reqx(**kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = "SELECT * FROM storage_support"
        sql, parameters = update_format_args(sql, kwargs)
        return con.execute(sql, parameters).fetchone()


def update_reqx(id, **kwargs):
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory
        sql = f"UPDATE storage_support SET"
        sql, parameters = update_format(sql, kwargs)
        parameters.append(id)
        con.execute(sql + "WHERE id = ?", parameters)
        con.commit()


# Преобразование полученного списка в словарь
def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


def update_format_where(sql, parameters: dict):
    sql += " WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())



####################################################################################################
##################################### ФОРМАТИРОВАНИЕ ЗАПРОСА #######################################
# Форматирование запроса без аргументов
def update_format(sql, parameters: dict):
    if "XXX" not in sql: sql += " XXX "

    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_args(sql, parameters: dict):
    sql = f"{sql} WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())

####################################################################################################


# Функция для создания Excel-файла на основе данных из базы данных
def create_excel_file():
    connection = sqlite3.connect(PATH_DATABASE)
    cursor = connection.cursor()

    # Получение данных из базы данных
    cursor.execute("SELECT * FROM storage_users")
    data = cursor.fetchall()

    # Создание нового Excel-файла
    wb = Workbook()
    ws = wb.active

    # Заголовки столбцов
    headers = [description[0] for description in cursor.description]
    ws.append(headers)

    # Заполнение данными
    for row in data:
        ws.append(row)

    # Сохранение файла
    excel_file_path = 'data.xlsx'
    wb.save(excel_file_path)

    # Закрытие соединения с базой данных
    connection.close()

    return excel_file_path
