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

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime, timedelta

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
    if email == 'test@example.com' and password == 'password123':
            # Redirect to the admin page
        return redirect(url_for('admin'))
    elif user:
        session['user_id'] = user[0]  # Store user ID in the session
        return redirect(url_for('home'))
    else:
        return "Invalid credentials. Please try again."

@app.route('/admin')
def admin():
    return render_template('admin.html')

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
"""@app.route('/details/<section>', methods=['GET', 'POST'])
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
"""
from datetime import datetime, timedelta

@app.route('/details/<section>', methods=['GET', 'POST'])
def details(section):
    conn = create_connection()
    cursor = conn.cursor()

    # Initialize variables
    itineraries = []
    section_title = ''
    section_content = ''
    show_form = False  # Initially show the destination and budget form
    show_itineraries_form = False  # Show the itineraries selection form after first submission
    selected_itineraries = []

    # Fetch all destinations from the Destination table
    cursor.execute("SELECT Destination_Id, Name FROM Destination")
    destinations = cursor.fetchall()

    if section == 'first':
        show_form=True
        section_title = 'Choose Your Destination'
        section_content = 'Select a destination and input your budget.'
        user_id = session.get('user_id')
        selected_destination = request.form.get('destination_id')
    if request.method == 'POST':
        if 'submit_destination' in request.form:
            # First form submission with destination and budget
            selected_destination = request.form.get('destination')
            budget = float(request.form.get('budget'))
            start_date = request.form.get('start_date')

            # Fetch itineraries within the specified budget for the chosen destination
            query = """
                SELECT Itinerary_Id, Activities, Budget, No_of_Dates
                FROM Itinerary
                WHERE Destination_Id = %s AND Budget <= %s
            """
            cursor.execute(query, (selected_destination, budget))
            itineraries = cursor.fetchall()

            # Show itineraries selection form
            show_form = False  # Hide the initial form
            show_itineraries_form = True  # Show itineraries selection form
            return render_template('details.html', 
                                   section=section,
                                   section_title=section_title, 
                                   section_content=section_content,
                                   destinations=destinations, 
                                   show_form=show_form,
                                   show_itineraries_form=show_itineraries_form,
                                   itineraries=itineraries,
                                   start_date=start_date)

        elif 'submit_itineraries' in request.form:
            # Second form submission with selected itineraries
            start_date = request.form.get('start_date')
            selected_itinerary_ids = request.form.getlist('selected_itinerary')
            selected_destination = request.form.get('destination_id')
            total_budget = 0
            total_days=0
            combined_activities = []
            itinerary_start_date = datetime.strptime(start_date, '%Y-%m-%d')

            for itinerary_id in selected_itinerary_ids:
                cursor.execute("SELECT Activities, Budget, No_of_Dates FROM Itinerary WHERE Itinerary_Id = %s", (itinerary_id,))
                itinerary = cursor.fetchone()
                activities, budget, no_of_days = itinerary
                total_budget += budget
                total_days += no_of_days
                combined_activities.append(activities)
                end_date = itinerary_start_date + timedelta(days=no_of_days)
                selected_itineraries.append((activities, itinerary_start_date.date(), end_date.date()))
                itinerary_start_date = end_date  # Update start date for next itinerary

            # Concatenate activities into a single string
            combined_activities_str = '; '.join(combined_activities)

            # Insert combined itinerary into the Itinerary table
            insert_query = """
                INSERT INTO Itinerary (Destination_Id, User_Id, Start_Date, No_of_Dates, Budget, Activities)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (selected_destination, user_id, start_date, total_days, total_budget, combined_activities_str))
            conn.commit()

            # Display chosen itineraries
            return render_template('chosen_itineraries.html', itineraries=selected_itineraries)

    return render_template('details.html', 
                           section=section, 
                           section_title=section_title, 
                           section_content=section_content, 
                           destinations=destinations, 
                           show_form=show_form,
                           show_itineraries_form=show_itineraries_form,
                           itineraries=itineraries)



@app.route('/chosen_itineraries')
def chosen_itineraries():
    conn = create_connection()
    cursor = conn.cursor()

    # Retrieve saved itineraries
    cursor.execute("SELECT Activities, Start_Date, End_Date FROM itinerary")
    itineraries = cursor.fetchall()

    return render_template('chosen_itineraries.html', itineraries=itineraries)
    


@app.route('/notify', methods=['GET', 'POST'])
def notify():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        destination_id = request.form.get('destination')
        user_id = session['user_id']

        # Update UserPreferences
        cursor.execute("INSERT INTO UserPreferences (User_Id, Preferences) VALUES (%s, %s) ON DUPLICATE KEY UPDATE Preferences = %s", 
                       (user_id, destination_id, destination_id))
        conn.commit()

        flash('Your preference has been saved. You will be notified when this destination becomes available.', 'success')
        return redirect(url_for('home'))

    # Fetch all destinations
    cursor.execute("SELECT Destination_Id, Name FROM Destination")
    destinations = cursor.fetchall()

    conn.close()
    return render_template('notify.html', destinations=destinations)


@app.route('/add_destination', methods=['POST'])
def add_destination():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        availability = int(request.form['availability'])  # Expect 1 or 0
        cost = float(request.form['cost'])

        conn = create_connection()
        cursor = conn.cursor()

        # Insert the new destination into the Destination table
        insert_query = """
            INSERT INTO Destination (Name, Location, Availability, Cost)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, location, availability, cost))
        conn.commit()

        # Redirect back to the admin page or a success page
        flash('Destination added successfully')
        return redirect(url_for('admin'))

    return render_template('admin.html')


@app.route('/add_itinerary', methods=['POST'])
def add_itinerary():
    if request.method == 'POST':
        # Retrieve form data
        destination_id = int(request.form['destination_id'])
        user_id = int(request.form['user_id'])
        start_date = request.form['start_date']
        no_of_dates = int(request.form['no_of_dates'])
        budget = float(request.form['budget'])
        activities = request.form['activities']

        # Connect to the database
        conn = create_connection()
        cursor = conn.cursor()

        # Insert the new itinerary into the Itinerary table
        insert_query = """
            INSERT INTO Itinerary (Destination_Id, User_Id, Start_Date, No_of_Dates, Budget, Activities)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (destination_id, user_id, start_date, no_of_dates, budget, activities))
        conn.commit()

        # Redirect back to the admin page or a success page
        return redirect(url_for('admin'))

    return render_template('admin.html')


@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the user session
    return redirect(url_for('login'))  # Redirect to the login page


if __name__ == '__main__':
    app.run(port=5030,debug=True)