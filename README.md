# Travel Planner – Full Stack DBMS Project

This is a full-stack travel planning web application that enables users to search for destinations, customize itineraries, manage bookings, and receive availability-based notifications. The project demonstrates complete integration of a relational database with frontend and backend components, supporting both user and admin workflows.

---

## Features

### 1. User Authentication
- Secure login and session management
- Special access credentials for admin users  
  *(Demo credentials: test@example.com / password123)*

### 2. Destination Search and Exploration
- Users can search destinations by name or location
- View key details: availability status, points of interest, estimated cost
- Visualize and compare travel options interactively

### 3. Itinerary Planning
- Input travel start and end dates
- Automatically calculates visit dates and displays possible itineraries
- Users select suitable options via checkboxes
- Selections are stored in the `Itinerary` table

### 4. Travel Mode Selection
- Supports transport preferences: bus, train, flight, etc.
- Integrated during the itinerary selection phase

### 5. Booking & Payment System
- Book selected itineraries through a dedicated booking page
- Payment information is stored as "paid through portal"
- Confirmation page shown post-booking
- Booking details tracked in the `Booking` table

### 6. Budget Calculator
- Computes trip budget dynamically based on stay duration and selected locations
- Budget is displayed and logged as part of the itinerary

### 7. Notification System
- Users can opt-in to be notified when destinations become available
- Automatic email notifications using SMTP
- Logged in the `Notification` table with timestamp and message

### 8. Admin Dashboard
- Add and manage destinations with ID, name, cost, availability, and location
- Create and manage itineraries linked to destinations
- View user bookings and system-wide itinerary data

---

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database:** MySQL  
- **Email System:** SMTP for notifications  

---

## Database Overview

Tables used in the system:
- `Users`
- `Destinations`
- `Itinerary`
- `Booking`
- `Notification`

---

## Getting Started

### Prerequisites
- Python 3.x
- MySQL Server
- SMTP-enabled email credentials (for notifications)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/alley2727/travel-planner-dbms.git
   cd travel-planner-dbms
