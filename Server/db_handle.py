import sqlite3


class DataBaseHandler():
    def __init__(self):
        self.connection=sqlite3.connect('rdp_db.db')
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS usersdata (
                id INTEGER PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            
            CREATE TABLE IF NOT EXISTS open_rooms (
                id INTEGER PRIMARY KEY,
                creator_address VARCHAR(255) NOT NULL
                creator_port INTEGER NOT NULL
                creator_type VARCHAR(255) NOT NULL
                password VARCHAR(255) NOT NULL
            )
            """)
        self.connection.commit()

    def login_check(self,username,password):
        try:
            result=self.connection.execute("SELECT * FROM usersdata WHERE username = ? AND password = ?",(username,password))
            fetched=result.fetchall()
            if fetched:
                return 'w'
            else:
                return 'noexist'
        except sqlite3.Error:
            return 'f'

        pass
    def register(self,username,hashed_password):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM usersdata WHERE username=?)", (username,))
            fetched = response.fetchone()[0]
            if fetched == 1:
                return 'exist'
            else:
                self.connection.execute("INSERT INTO usersdata (username,password) \ VALUES (?,?)",(username,hashed_password))
                self.connection.commit()
                return 'w'
        except sqlite3.Error:
            return 'f'

    def delete_user(self,username):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM usersdata WHERE username=?)", (username,))
            fetched = response.fetchone()[0]
            if fetched == 1: #exists
                self.connection.execute("DELETE from usersdata where username = ?;",(username,))
                self.connection.commit()
                return 'w'
            else:
                return 'noexist'
        except sqlite3.Error:
            return 'f'


    def create_room(self,address,port,type,password):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM open_rooms WHERE creator_address = ? AND creator_port = ? AND creator_type = ? AND password = ? )", (address, port, type, password))
            fetched = response.fetchone()[0]
            if fetched == 1:
                return 'exist'
            else:
                self.connection.execute("INSERT INTO open_rooms (creator_address,creator_port,creator_type,password) \ VALUES (?,?)",(address, port,type,password))
                self.connection.commit()
                return 'w'
        except sqlite3.Error:
            return 'f'
    def end_room(self,address,port,type,password):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM open_rooms WHERE creator_address = ? AND creator_port = ? AND creator_type = ? AND password = ? )", (address, port, type, password))
            fetched = response.fetchone()[0]
            if fetched == 1: #exists
                self.connection.execute("DELETE from open_rooms WHERE creator_address = ? AND creator_port = ? AND creator_type = ? AND password = ?;", (address, port, type, password))
                self.connection.commit()
                return 'w'
            else:
                return 'noexist'
        except sqlite3.Error:
            return 'f'

    def enter_room(self,password):
        try:
            response = self.connection.execute("SELECT EXISTS(SELECT 1 FROM open_rooms WHERE password = ? )", (password,))
            fetched = response.fetchone()[0]
            if fetched == 1: #exists
                room_data=self.connection.execute("SELECT * FROM open_rooms WHERE password = ?;", (password,))
                fetched_data=room_data.fetchall()
                address=fetched_data[1]
                port=fetched_data[2]
                peer_type=fetched_data[3]
                status=self.end_room(address,port,peer_type,password)
                if status == 'w':
                    return (address,port,peer_type)
                elif status == 'noexist' or status == 'f':
                    return 'noendroom'
            else:
                return 'noexist'
        except sqlite3.Error:
            return 'f'
