from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime, timedelta
import notification

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
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('select count(*) from destination')
    data={"number":cursor.fetchone()[0]}
    if 'user_id' in session:
        return render_template('home.html',data=data)
        #return f"Welcome, User ID: {session['user_id']}! This is your home page."
    #else:
        #return redirect(url_for('index'))


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
    
#notification maithri sent
@app.route('/notify', methods=['GET', 'POST'])
def notify():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        destination_id = request.form.get('destination')
        user_id = session['user_id']

        # Update UserPreferences with user's chosen destination
        cursor.execute("""
            INSERT INTO UserPreferences (User_Id, Preferences)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE Preferences = %s
        """, (user_id, destination_id, destination_id))
        conn.commit()

        flash('Your preference has been saved. You will be notified when this destination becomes available.', 'success')
        return redirect(url_for('home'))

    # Fetch available destinations to display in the form
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

@app.route('/delete_destination', methods=['POST'])
def delete_destination():
    destination_id = int(request.form['destination_id'])

    conn = create_connection()
    cursor = conn.cursor()

    # Delete the destination from the Destination table
    delete_query = "DELETE FROM Destination WHERE Destination_Id = %s"
    cursor.execute(delete_query, (destination_id,))
    conn.commit()

    flash('Destination deleted successfully')
    return redirect(url_for('admin'))
@app.route('/delete_itinerary', methods=['POST'])
def delete_itinerary():
    itinerary_id = int(request.form['itinerary_id'])
    user_id = int(request.form['user_id'])

    conn = create_connection()
    cursor = conn.cursor()

    # Delete the itinerary from the Itinerary table
    delete_query = "DELETE FROM Itinerary WHERE Itinerary_Id = %s AND User_Id = %s"
    cursor.execute(delete_query, (itinerary_id, user_id))
    conn.commit()

    flash('Itinerary deleted successfully')
    return redirect(url_for('admin'))
@app.route('/update_destination', methods=['POST'])
def update_destination():
    destination_id = int(request.form['destination_id'])
    name = request.form['name']
    location = request.form['location']
    availability = int(request.form['availability'])
    cost = float(request.form['cost'])

    conn = create_connection()
    cursor = conn.cursor()

    # Update the destination in the Destination table
    update_query = """
        UPDATE Destination
        SET Name = %s, Location = %s, Availability = %s, Cost = %s
        WHERE Destination_Id = %s
    """
    cursor.execute(update_query, (name, location, availability, cost, destination_id))
    conn.commit()

    flash('Destination updated successfully')
    notification.send_notification_emails()
    #cursor.execute("TRUNCATE notification")
    conn.commit()
    print("notifs sent")
    return redirect(url_for('admin'))

@app.route('/update_itinerary', methods=['POST'])
def update_itinerary():
    itinerary_id = int(request.form['itinerary_id'])
    destination_id = int(request.form['destination_id'])
    user_id = int(request.form['user_id'])
    start_date = request.form['start_date']
    no_of_dates = int(request.form['no_of_dates'])
    budget = float(request.form['budget'])
    activities = request.form['activities']

    conn = create_connection()
    cursor = conn.cursor()

    # Update the itinerary in the Itinerary table
    update_query = """
        UPDATE Itinerary
        SET Destination_Id = %s, User_Id = %s, Start_Date = %s, No_of_Dates = %s, Budget = %s, Activities = %s
        WHERE Itinerary_Id = %s
    """
    cursor.execute(update_query, (destination_id, user_id, start_date, no_of_dates, budget, activities, itinerary_id))
    conn.commit()

    flash('Itinerary updated successfully')
    return redirect(url_for('admin'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the user session
    return redirect(url_for('login'))  # Redirect to the login page









@app.route('/view_details', methods=['GET', 'POST'])
def view_details():
    user_id = session.get('user_id')  # Assume user_id is stored in session after login
    print(f"User ID: {user_id}")  # Debug: Check if user ID is retrieved from session

    if user_id:
        conn = create_connection()
        cursor = conn.cursor()

        # Query to fetch the last added itinerary details for the logged-in user
        query = """
            SELECT Itinerary_Id, Activities, Budget
            FROM Itinerary
            WHERE User_Id = %s
            ORDER BY Itinerary_Id DESC
            LIMIT 1
        """
        print("Executing itinerary fetch query...")  # Debug
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        print(f"Query Result: {result}")  # Debug: Check if the itinerary details are fetched

        if result:
            itinerary_id, activities, budget = result
            print(f"Itinerary ID: {itinerary_id}, Activities: {activities}, Budget: {budget}")  # Debug

            # Handle "Pay Now" or "Cancel" action
            if request.method == 'POST':
                payment_confirmation = request.form.get('payment_confirmation')
                print(f"Payment Confirmation: {payment_confirmation}")  # Debug

                # Determine booking status and payment status
                if payment_confirmation == 'confirmed':
                    payment_status = "Paid"
                    booking_status = "Confirmed"
                    flash("Payment confirmed. Your booking is successful.")
                else:
                    payment_status = "Not Paid"
                    booking_status = "Unsuccessful"
                    flash("Payment was canceled. Your booking was not completed.")

                booking_date = datetime.now().date()
                print(f"Calling stored procedure AddBooking with parameters: itinerary_id={itinerary_id}, user_id={user_id}, payment_status={payment_status}, booking_status={booking_status}, booking_date={booking_date}")  # Debug

                # Call the stored procedure to insert booking data
                try:
                    cursor.callproc('AddBooking', [itinerary_id, user_id, payment_status, booking_status, booking_date])
                    conn.commit()
                    print("Stored procedure executed successfully")  # Debug
                except Exception as e:
                    print(f"Error calling stored procedure: {e}")  # Debug: Print any errors
                    flash("There was an error processing your booking. Please try again.")
                
                return redirect(url_for('view_details'))

            conn.close()
            return render_template('view_details.html', activities=activities, budget=budget)
        else:
            conn.close()
            print("No itinerary found for user")  # Debug
            return render_template('view_details.html', error="No itinerary found.")
    else:
        print("User not logged in, redirecting to login page")  # Debug
        return redirect(url_for('login'))






def get_itineraries_with_destinations():
    """Run a join query to get itineraries with destination names."""
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT i.Itinerary_Id, i.Start_Date, i.Budget, d.Name AS Destination_Name
        FROM Itinerary i
        JOIN Destination d ON i.Destination_Id = d.Destination_Id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

def get_users_with_high_budget_itineraries():
    """Run a nested query to get users with itineraries above the average budget."""
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT DISTINCT u.User_Id, u.First_Name, u.Last_Name
        FROM User u
        JOIN Booking b ON u.User_Id = b.User_Id
        WHERE b.Itinerary_Id IN (
            SELECT Itinerary_Id
            FROM Itinerary
            WHERE Budget > (SELECT AVG(Budget) FROM Itinerary)
        )
    """
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results

@app.route('/query_results')
def query_results():
    join_results = get_itineraries_with_destinations()
    nested_results = get_users_with_high_budget_itineraries()
    return render_template('query_results.html', join_results=join_results, nested_results=nested_results)



if __name__ == '__main__':
    app.run(port=5030,debug=True)