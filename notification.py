import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import logging

logging.basicConfig(filename='notification.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            database='TravelPlanner'
        )
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None


def send_notification_emails():
    conn = create_connection()
    if not conn:
        print("no connection")
        return

    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch unsent notifications created within the last hour
        cursor.execute("""
            SELECT n.Notification_Id, n.Message, u.Email, d.Name as DestinationName
            FROM Notification n
            JOIN User u ON n.User_Id = u.User_Id
            JOIN Destination d ON n.Destination_Id = d.Destination_Id
        """)
        notification = cursor.fetchone()

        print(notification)
        subject = f"TravelEase Notification: Destination Available"
        message = f"""
        Dear Traveler,

        {notification['Message']}

        Destination: {notification['DestinationName']}

        Log in to your TravelEase account to view more details and book your trip!

        Best regards,
        The TravelEase Team
        """
        
        send_email(notification['Email'], subject, message)

    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

def send_email(to_email, subject="I am manya", message="hello manya"):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "manyasingh1711@gmail.com"
    sender_password = "qdkx yujk yxgb xwwk"

    email_message = MIMEMultipart()
    email_message["From"] = sender_email
    email_message["To"] = to_email
    email_message["Subject"] = subject
    email_message.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        logging.info(f"Notification email sent to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")
        return False