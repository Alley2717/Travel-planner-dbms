import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2004',
            database='TravelPlanner'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def add_user(connection, email, password, first_name, last_name):
    cursor = connection.cursor()
    query = "INSERT INTO User (Email, Password, First_Name, Last_Name) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (email, password, first_name, last_name))
    connection.commit()
    return cursor.lastrowid

if __name__ == "__main__":
    conn = create_connection()
    user_id = add_user(conn, 'test@example.com', 'password123', 'John', 'Doe')
    print(f"User created with ID: {user_id}")
