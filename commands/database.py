import sqlite3

class Database:
    def __init__(self):
        self._initialize_db()

    def _connect(self):
        """Connect to the database and return the connection and cursor."""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        return conn, cursor

    def _initialize_db(self):
        """Initialize the database tables if they don't already exist."""
        conn, cursor = self._connect()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            is_admin INTEGER NOT NULL DEFAULT 0
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS premium_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                command TEXT UNIQUE NOT NULL,
                description TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authorized_groups (
                group_id INTEGER PRIMARY KEY
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authorized_users (
                user_id INTEGER PRIMARY KEY,
                username TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banned_users (
                username TEXT PRIMARY KEY
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gateways (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                format TEXT,
                condition TEXT,
                comment TEXT,
                type TEXT,
                amount TEXT
            )
        """)
        conn.commit()
        conn.close()

    def add_admin(self, username):
        conn, cursor = self._connect()
        cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", (f"@{username}",))
        conn.commit()
        conn.close()

    def insert_gateways(self):
        conn, cursor = self._connect()
        gateways_data = [
        ("Onyx Auth", "$au card|month|year|cvv", "ON! ✅", "Online API Gate!", "Free-Plan", "$1"),
        ("Braintree", "$mix card|month|year|cvv", "ON! ✅", "Online API Gate!", "Free-Plan", "$10"),
        ("Braintree Auth V1", "$xe card|month|year|cvv", "ON! ✅", "Online API Gate!", "Premium-Plan", "$20"),
        ("Payflow AVS", "$mar card|month|year|cvv", "ON! ✅", "Online API Gate!", "VIP-Plan", "$30"),
        # Add more gateways if needed
        ]

        # Insert data into the database
        cursor.executemany('''
            INSERT OR IGNORE INTO gateways (name, format, condition, comment, type, amount)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', gateways_data)
        conn.commit()
        conn.close()

    def remove_admin(self, username):
        conn, cursor = self._connect()
        cursor.execute("DELETE FROM users WHERE username = ?", (f"@{username}",))
        conn.commit()
        conn.close()

    def get_admin(self):
        """Check if there is an admin in the database."""
        conn, cursor = self._connect()
        cursor.execute("SELECT user_id FROM users WHERE is_admin = 1")
        admin = cursor.fetchone()
        conn.close()
        return  admin if admin else None
    
    def is_admin(self, user_id):
        conn, cursor = self._connect()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ? AND is_admin = 1", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def is_owner(self, user_id):
        conn, cursor = self._connect()
        cursor.execute("select user_id from users where id = 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] == user_id

    def register_user(self, user_id, username, is_admin=0):
        """Add a user to the database."""
        conn, cursor = self._connect()
        cursor.execute("INSERT OR REPLACE INTO users (user_id, username, is_admin) VALUES (?, ?, ?)", 
                    (user_id, f"@{username}", is_admin))
        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        """Delete a user from the database."""
        conn, cursor = self._connect()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

    def get_user(self, user_id):
        """Get a user from the database."""
        conn, cursor = self._connect()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_user_by_username(self, username):
        conn, cursor = self._connect()
        cursor.execute("SELECT * FROM users WHERE username = ?", (f"@{username}",))
        user = cursor.fetchone()
        conn.close()
        return user

    def get_admins(self):
        conn, cursor = self._connect()
        cursor.execute("SELECT user_id FROM users WHERE is_admin = 1")
        admins = cursor.fetchall()
        conn.close()
        return admins

    def add_premium_command(self, command, description):
        conn, cursor = self._connect()
        cursor.execute("INSERT OR IGNORE INTO premium_commands (command, description) VALUES (?, ?)", (command, description))
        conn.commit()
        conn.close()

    def delete_premium_command(self, command):
        conn, cursor = self._connect()
        cursor.execute("DELETE FROM premium_commands WHERE command = ?", (command,))
        conn.commit()
        conn.close()

    def get_premium_commands(self):
        conn, cursor = self._connect()
        cursor.execute("SELECT command, description FROM premium_commands")
        commands = [{"command": row[0], "description": row[1]} for row in cursor.fetchall()]
        conn.close()
        return commands

    def get_premium_command(self, command_name):
        """
        Fetch command from the database.
        Return the command details if it exists, else None.
        """
        conn, cursor = self._connect()
        cursor.execute("SELECT command_name, description FROM premium_commands WHERE command_name = ?", (command_name,))
        result = cursor.fetchone()
        
        conn.close()
        return result if result else None

    def update_premium_command(self, command_name, new_description):
        """
        Update the command description in the database.
        Returns True if the update was successful, False otherwise.
        """
        conn, cursor = self._connect() 
        if self.get_premium_command(command_name) is None:
            return False   
        cursor.execute("UPDATE premium_commands SET description = ? WHERE command_name = ?", (new_description, command_name))
        conn.commit()
        updated = cursor.rowcount > 0  # Check if any row was updated
        
        conn.close()
        return updated

    def authorize_group(self, group_id):
        conn, cursor = self._connect()
        cursor.execute("INSERT OR IGNORE INTO authorized_groups (group_id) VALUES (?)", (group_id,))
        conn.commit()
        conn.close()

    def unauthorize_group(self, group_id):
        conn, cursor = self._connect()
        cursor.execute("DELETE FROM authorized_groups WHERE group_id = ?", (group_id,))
        conn.commit()
        conn.close()

    def authorize_user(self, user_id,username):
        conn, cursor = self._connect()
        cursor.execute("INSERT OR IGNORE INTO authorized_users (user_id,username) VALUES (?, ?)", (user_id, f"@{username}",))
        conn.commit()
        conn.close()

    def unauthorize_user(self, username):
        
        conn, cursor = self._connect()
        cursor.execute("DELETE FROM authorized_users WHERE username = ?", (f"@{username}",))
        conn.commit()
        conn.close()

    def ban_user(self, username):
        conn, cursor = self._connect()
        cursor.execute("INSERT OR IGNORE INTO banned_users (username) VALUES (?)", (f"@{username}",))
        conn.commit()
        conn.close()

    def unban_user(self, username):        
        conn, cursor = self._connect()
        cursor.execute("DELETE FROM banned_users WHERE user_id = ?", (f"@{username}",))
        conn.commit()
        conn.close()

# Instantiate the Database class
db = Database()
