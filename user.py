import sqlite3


def get_user_by_username(username):
    with sqlite3.connect("mydatabase.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_models WHERE username = ?", (username,))
        return cursor.fetchone()


def create_user(username, age, like_1=0, like_2=0, like_3=0, like_4=0, like_5=0):
    with sqlite3.connect("mydatabase.db") as conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO user_models (username, age, like_1, like_2, like_3, like_4, like_5)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(sql, (username, age, like_1, like_2, like_3, like_4, like_5))
        conn.commit()


'''
# Connect to the database
conn = sqlite3.connect("user_models.db")

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Define the SQL statement to create the user_models table
sql = """CREATE TABLE user_models (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  age INTEGER NOT NULL,
  like_1 INTEGER DEFAULT 0,
  like_2 INTEGER DEFAULT 0,
  like_3 INTEGER DEFAULT 0,
  like_4 INTEGER DEFAULT 0,
  like_5 INTEGER DEFAULT 0
)"""

# Execute the SQL statement
cursor.execute(sql)

# Commit the changes to the database
conn.commit()

print("Table 'user_models' created successfully.")
'''
