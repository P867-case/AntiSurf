import sqlite3

class Api:
    def __init__(self, file):
        self.file = file
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()

    def add_website(self, url) -> bool:
        if 'www' in url:
            self.cursor.execute('INSERT INTO Source (domain) VALUES (?)',(url.replace('www.',''), ))
            self.cursor.execute('INSERT INTO Source (domain) VALUES (?)',(url, ))
        else:
            self.cursor.execute('INSERT INTO Source (domain) VALUES (?)', (url,))
            self.cursor.execute('INSERT INTO Source (domain) VALUES (?)', (f'www.{url}',))
        self.connection.commit()
        return True

    def get_all_website(self) -> list:
        self.cursor.execute('SELECT * FROM Source')
        urls = self.cursor.fetchall()
        return urls

    def update_user_info(self, login, parm, option) -> bool:
        try:
            self.cursor.execute(
                f"UPDATE Users SET {parm} = ? WHERE login = ?",
                (option, login)
            )
            return True
            self.connection.commit()
        except Exception as e:
            return False

    def create_user(self, login, password) -> list:
        try:
            self.cursor.execute(
                'INSERT INTO User (login, password) VALUES (?, ?)',
                (login, password)
            )
            self.connection.commit()
            return [True, 'Пользователь создан!']
        except Exception as e:
            return [False, f'Error: {e}\nОбратитесь к разработчику']

    def remove_website(self, source) -> bool:
        if 'www' in source:
            self.cursor.execute(
                'DELETE FROM Source WHERE domain = ?',
                (source,)
            )
            self.cursor.execute(
                'DELETE FROM Source WHERE domain = ?',
                (source.replace("www.",''),)
            )
        else:
            self.cursor.execute(
                'DELETE FROM Source WHERE domain = ?',
                (source,)
            )
            self.cursor.execute(
                'DELETE FROM Source WHERE domain = ?',
                (f'www.{source}',)
            )
        self.connection.commit()
        return True

    def get_user(self):
        self.cursor.execute("SELECT * FROM User")
        return self.cursor.fetchone()

    def reconnect(self):
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()
