import sqlite3
from tgbot.data.config import PATH_DATABASE



def db():
    conn = sqlite3.connect(PATH_DATABASE)
    cur = conn.cursor()
    if len(cur.execute("PRAGMA table_info(storage_users)").fetchall()) == 8:
        print("DB storage_users was found | (1/4)")
    else:
        cur.execute("CREATE TABLE IF NOT EXISTS storage_users("
                    "id INTEGER PRIMARY KEY,"
                    "reg_date TEXT,"
                    "user_id INTEGER,"
                    "user_login TEXT,"
                    "user_name TEXT,"
                    "contact_name TEXT,"
                    "contact_phone_number INTEGER,"
                    "alarm_time TEXT)")
        print("DB storage_users was not found | (1/4) | Creating...")
    if len(cur.execute("PRAGMA table_info(bot_settings)").fetchall()) == 2:
        print("DB bot_settings was found | (2/4)")
    else:
        cur.execute("CREATE TABLE IF NOT EXISTS bot_settings("
                    "alarm_date TEXT,"
                    "cheap_day TEXT)")
        print("DB bot_settings was not found | (2/4) | Creating...")
    if len(cur.execute("PRAGMA table_info(storage_transaction)").fetchall()) == 8:
        print("DB storage_transaction was found | (3/4)")
    else:
        cur.execute("CREATE TABLE IF NOT EXISTS storage_transaction("
                    "id INTEGER PRIMARY KEY,"
                    "user_id INTEGER,"
                    "user_name TEXT,"
                    "order_date TEXT,"
                    "order_id INTEGER,"
                    "liqpay_order_id INTEGER,"
                    "order_amount INTEGER,"
                    "order_status TEXT)")
        print("DB storage_transaction was not found | (3/4) | Creating...")
    if len(cur.execute("PRAGMA table_info(storage_support)").fetchall()) == 6:
        print("DB storage_support was found | (4/4)")
    else:
        cur.execute("CREATE TABLE IF NOT EXISTS storage_support("
                    "id INTEGER PRIMARY KEY,"
                    "user_id INTEGER,"
                    "user_name TEXT,"
                    "text TEXT,"
                    "status TEXT,"
                    "date TEXT)")
        print("DB storage_support was not found | (4/4) | Creating...")

    conn.commit()

    cur.close()
    conn.close()




