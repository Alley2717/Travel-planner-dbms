Travel Planner – DBMS Project

This web application is a full-stack travel planning system that helps users explore destinations, customize itineraries, manage bookings, and receive notifications based on availability and preferences. Built using a relational database management system, the project covers both user and admin functionalities and includes real-time updates and budget-aware planning.

Key Features
1. User Authentication
- Secure login system with special access for admin users.
- Admin credentials: test@example.com and password123.

2. Destination Search and Exploration
Users can search for destinations and view:
- Location information
- Availability status
- Places to visit within the destination

3. Itinerary Planning
- Users enter start date and end date.
- The system calculates visit dates for each place based on stay duration.
- Displays all itineraries within budget as checkboxes for selection.
- Selected itineraries are saved in the Itinerary table.

4. Travel Mode Selection
- Users can select their preferred mode of transport (bus, train, flight, etc.) during planning.

5. Booking System
- Chosen itinerary can be booked via a booking page.
- Payment information is stored (always marked as "paid through portal").
- Booking and payment status are tracked in the Booking table.
- A confirmation page displays after successful booking.

6. Budget Calculation
- Budget is automatically calculated based on selected destinations and number of days.
- The total is stored and displayed as part of the itinerary details.

7. Notification System
- Users can choose to be notified when an unavailable destination becomes available.
- When availability is updated, an email is triggered to the user.
- Notification details are logged in the Notification table with timestamp and message.

8. Admin Dashboard
Admin can:
- Add destinations with details like ID, name, location, availability, and cost.
- Add itineraries linked to destinations.
- View and manage all itineraries and bookings.

Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Database: MySQL
- Email Handling: SMTP (for notification system)

