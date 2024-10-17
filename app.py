""" 

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Make sure your MySQL credentials are correct
            #password='2004',
            database='TravelPlanner'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def add_user(connection, email, password, first_name, last_name):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO User (Email, Password, First_Name, Last_Name) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email, password, first_name, last_name))
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_user', methods=['POST'])
def submit_user():
    conn = create_connection()
    if conn is None:
        return "Error connecting to the database"

    # Retrieve form data
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    # Add user to the database
    user_id = add_user(conn, email, password, first_name, last_name)
    
    if user_id:
        return f"User created with ID: {user_id}"
    else:
        return "There was an error creating the user."

if __name__ == '__main__':
    app.run(debug=True) """

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Make sure your MySQL credentials are correct
            #password='2004',
            database='TravelPlanner'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def add_user(connection, email, password, first_name, last_name):
    cursor = connection.cursor()
    try:
        query = "INSERT INTO User (Email, Password, First_Name, Last_Name) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email, password, first_name, last_name))
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"An error occurred: {e}")
        return None

def authenticate_user(connection, email, password):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM User WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"An error occurred: {e}")
        return None
""" 
@app.route('/')
def index():
    return render_template('index.html') """
# Route for the loading page
@app.route('/')
def loading_page():
    return render_template('loading.html')

# Route for the login/signup page (after loading)
@app.route('/login')
def login_page():
    return render_template('index.html')


@app.route('/submit_user', methods=['POST'])
def submit_user():
    conn = create_connection()
    if conn is None:
        return "Error connecting to the database"

    # Retrieve form data
    email = request.form['email']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    # Add user to the database
    user_id = add_user(conn, email, password, first_name, last_name)
    
    if user_id:
        return f"User created with ID: {user_id}"
    else:
        return "There was an error creating the user."

@app.route('/login', methods=['POST'])
def login():
    conn = create_connection()
    if conn is None:
        return "Error connecting to the database"

    # Retrieve login data
    email = request.form['email']
    password = request.form['password']

    # Authenticate user
    user = authenticate_user(conn, email, password)

    if user:
        session['user_id'] = user[0]  # Store user ID in the session
        return redirect(url_for('home'))
    else:
        return "Invalid credentials. Please try again."

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
        #return f"Welcome, User ID: {session['user_id']}! This is your home page."
    #else:
        #return redirect(url_for('index'))

""" @app.route('/details/<section>')
def details(section):
    section_title = ''
    section_content = ''

    # Dynamically set content based on which button was clicked
    if section == 'first':
        section_title = 'First Section Details'
        section_content = 'This is some content about the first section.'
    elif section == 'second':
        section_title = 'Second Section Details'
        section_content = 'This is some content about the second section.'
    elif section == 'third':
        section_title = 'Third Section Details'
        section_content = 'This is some content about the third section.'

    return render_template('details.html', section=section, section_title=section_title, section_content=section_content)
 """
@app.route('/details/<section>', methods=['GET', 'POST'])
def details(section):
    conn = create_connection()
    cursor = conn.cursor()

    # Fetching all destinations from the Destination table
    cursor.execute("SELECT Destination_Id, Name FROM Destination")
    destinations = cursor.fetchall()

    if request.method == 'POST':
        selected_destination = request.form.get('destination')
        budget_range = request.form.get('budget')

        # Logic to handle the form submission, filtering destinations within the budget, etc.
        # For now, just display the selected values as feedback
        return f"Selected destination: {selected_destination}, Budget: {budget_range}"

    return render_template('details.html', section=section, destinations=destinations)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5020,debug=True)
