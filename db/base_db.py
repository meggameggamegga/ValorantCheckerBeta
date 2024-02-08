import sqlite3



class DataBase:
    def __init__(self,db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        with self.connect:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    user_name TEXT,
                                    language TEXT
                                    count_check INT DEFAULT 0
                                )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS sell_accs (
                                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id     INTEGER,
                                    label_acc   TEXT,
                                    login       TEXT,
                                    password    TEXT,
                                    price_buyer INTEGER,
                                    status      TEXT,
                                    buyer_id    INTEGER
                                )''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS subs (
                                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                photo   TEXT,
                                timepay TEXT
                                )''')

    def user_exist(self,user_id):
        with self.connect:
            data = self.cursor.execute('''SELECT user_id,user_name FROM users WHERE user_id=(?)''',
                                [user_id]).fetchall()
            return data if data else False

    def add_user(self,user_id,user_name):
        with self.connect:
            return self.cursor.execute('''INSERT INTO users(user_id,user_name,language) VALUES (?,?,?)''',
                                       [user_id,user_name,'RU'])

    def get_users(self):
        with self.connect:
            return self.cursor.execute('''SELECT * FROM users''').fetchall()

    def set_language(self, user_id, lang):
        with self.connect:
            return self.cursor.execute('''UPDATE users SET language = ? WHERE user_id = ?''',
                                       [lang, user_id])

    def get_language(self, user_id):
        with self.connect:
            try:
                language = self.cursor.execute('''SELECT language FROM users WHERE user_id=(?)''',
                                           [user_id]).fetchone()[0]
            except Exception as e:
                language = 'RU'
            return language

    def set_seller(self,user_id,role_id):
        with self.connect:
            return self.cursor.execute('''UPDATE users SET role_id=(?) WHERE user_id=(?)''',
                                       [role_id,user_id])

    def delete_seller(self,user_id,role_id):
        with self.connect:
            return self.cursor.execute('''UPDATE users SET role_id=(?) WHERE user_id=(?)''',
                                   [role_id, user_id])
    #МБ НЕ ВОРК
    def get_selleres(self):
        with self.connect:
            return self.cursor.execute('''SELECT id,user_id,user_name FROM users WHERE role_id=(2) ''').fetchall()

    def add_check_acc(self,user_id,count):
        with self.connect:
            return self.cursor.execute('''UPDATE users SET count_check=(?) WHERE user_id=(?)''',
                                       [count,user_id])

    def get_count_check(self,user_id):
        with self.connect:
            return self.cursor.execute('''SELECT count_check FROM users WHERE user_id=(?)''',
                                       [user_id]).fetchone()
    def get_all_checks(self):
        with self.connect:
            counts = self.cursor.execute('''SELECT count_check FROM users''').fetchall()
            count = [el[0] for el in counts]
            return sum(count)
#----------------------------------SELL_ACCOUNTS-----------------------------------

    def add_account(self,user_id,login,password,label,status,buyer_id):
        with self.connect:
            return self.cursor.execute('''INSERT INTO sell_accs(user_id,login,password,label_acc,status,buyer_id) VALUES(?,?,?,?,?,?)''',
                                       [user_id,login,password,label,status,buyer_id])

    def get_account_data(self,user_id,label):
        with self.connect:
            return self.cursor.execute('''SELECT login,password,label_acc FROM sell_accs WHERE user_id=(?) AND label_acc=(?)''',
                                       [user_id,label]).fetchone()

    def add_account_price(self,user_id,label,price_buyer,buyer_id):
        with self.connect:
            return self.cursor.execute('''UPDATE sell_accs SET price_buyer=(?) WHERE user_id=(?) AND label_acc=(?) AND buyer_id=(?)''',
                                       [price_buyer,user_id,label,buyer_id])
    def set_status(self,user_id,label,status,buyer_id):
        with self.connect:
            return self.cursor.execute('''UPDATE sell_accs SET status=(?) WHERE user_id=(?) AND label_acc=(?) AND buyer_id=(?)''',
                                       [status,user_id,label,buyer_id])
    def get_status(self,user_id,label):
        with self.connect:
            return self.cursor.execute('''SELECT status FROM sell_accs WHERE user_id=(?) AND label_acc=(?)''',
                                       [user_id,label]).fetchone()
    #БРАТЬ ID БАЕРОВ ПО ПРАЙСУ И ПО ЮЗЕРА ID КЛИЕНТА
    def get_buyer_id_label(self,client_id,price,label):
        with self.connect:
            return self.cursor.execute('''SELECT buyer_id FROM sell_accs WHERE user_id=(?) AND label_acc=(?) AND price_buyer=(?)''',
                                       [client_id,label,price]).fetchall()

    def get_buyer_id(self,user_id,role_id=2):
        with self.connect:
            return self.cursor.execute('''SELECT id FROM users WHERE user_id=(?) AND role_id=(?)''',
                                       [user_id,role_id]).fetchone()
    def set_status_seller(self,status,label,buyer_id):
        with self.connect:
            return self.cursor.execute('''UPDATE sell_accs SET status=(?) WHERE buyer_id=(?) AND label_acc=(?)''',
                                       [status,buyer_id,label])
    def get_statuses_labels(self,label):
        with self.connect:
            return self.cursor.execute('''SELECT status FROM sell_accs WHERE label_acc=(?)''',
                                       [label]).fetchall()
    def get_status_buyer(self,label):
        with self.connect:
            return self.cursor.execute('''SELECT status,buyer_id FROM sell_accs WHERE label_acc=(?)''',
                                       [label]).fetchall()
    def get_cur_status(self,label,buyer_id):
        with self.connect:
            return self.cursor.execute('''SELECT status FROM sell_accs WHERE label_acc=(?) AND buyer_id=(?)''',
                                       [label,buyer_id]).fetchone()
#----------------------------------SUBS------------------------------#

    def add_user_pay(self,user_id,photo,timepay):
        with self.connect:
            return self.cursor.execute('''INSERT INTO subs(user_id,photo,timepay) VALUES(?,?,?)''',
                                       [user_id,photo,timepay])
    def accept_pay(self,timepay,user_id):
        with self.connect:
            data = self.cursor.execute('''UPDATE subs SET timepay=(?) WHERE user_id=(?)''',
                                       [timepay,user_id]).fetchone()
            return data
    def delete_pay(self,user_id):
        with self.connect:
            return self.cursor.execute('''DELETE FROM subs WHERE user_id=(?)''',
                                       [user_id]).fetchone()
    def get_all_subs(self):
        with self.connect:
            return self.cursor.execute('''SELECT user_id,timepay FROM subs''').fetchall()

    def get_cur_sub(self,user_id):
        with self.connect:
            data = self.cursor.execute('''SELECT user_id,timepay FROM subs WHERE user_id=(?)''',
                                       [user_id]).fetchone()
            return data if data else None