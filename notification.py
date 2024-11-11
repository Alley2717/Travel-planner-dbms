import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='notification.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

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
        return

    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch new unsent notifications
        cursor.execute("""
            SELECT n.*, u.Email, d.Name as DestinationName
            FROM Notification n
            JOIN User u ON n.User_Id = u.User_Id
            JOIN Destination d ON n.Destination_Id = d.Destination_Id
            WHERE n.Timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR)
            AND n.Sent = FALSE
        """)
        notifications = cursor.fetchall()

        for notification in notifications:
            subject = f"TravelEase Notification: {notification['Type']}"
            message = f"""
            Dear Traveler,

            {notification['Message']}

            Destination: {notification['DestinationName']}

            Log in to your TravelEase account to view more details and book your trip!

            Best regards,
            The TravelEase Team
            """
            
            # Send email to the user
            if send_email(notification['Email'], subject, message):
                # Log the notification with the send time
                logging.info(f"Notification sent to {notification['Email']} for {notification['DestinationName']} at {datetime.now()}")

                # Mark notification as sent
                cursor.execute("""
                    UPDATE Notification 
                    SET Sent = TRUE 
                    WHERE Notification_Id = %s
                """, (notification['Notification_Id'],))
                conn.commit()

    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
    finally:
        cursor.close()
        conn.close()

def send_email(to_email, subject, message):
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "manyasingh1711@gmail.com"
    sender_password = "qdkx yujk yxgb xwwk"  # Use an app password for Gmail

    # Create the email message
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
        print(f"Email sent to {to_email}")  # For immediate confirmation
        return True
    except Exception as e:
        logging.error(f"Error sending email to {to_email}: {e}")
        print(f"Failed to send email: {e}")  # For debugging
        return False


if __name__ == "__main__":
    # Send unsent notifications as emails
    send_notification_emails()
