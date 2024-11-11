CREATE DATABASE TravelPlanner;

USE TravelPlanner;

CREATE TABLE User (
    User_Id INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255)
);

CREATE TABLE Destination (
    Destination_Id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Location VARCHAR(255),
    Availability BOOLEAN,
    Cost DECIMAL(10, 2)
);

CREATE TABLE UserPreferences (
    User_Id INT,
    Preferences TEXT,
    FOREIGN KEY (User_Id) REFERENCES User(User_Id)
);

CREATE TABLE Itinerary (
    Itinerary_Id INT AUTO_INCREMENT PRIMARY KEY,
    Destination_Id INT,
    User_Id INT,
    Start_Date DATE,
    No_of_Dates INT,
    Budget DECIMAL(10, 2),
    Activities TEXT,
    FOREIGN KEY (Destination_Id) REFERENCES Destination(Destination_Id),
    FOREIGN KEY (User_Id) REFERENCES User(User_Id)
);

CREATE TABLE ItineraryActivities (
    Itinerary_Id INT,
    Activities TEXT,
    FOREIGN KEY (Itinerary_Id) REFERENCES Itinerary(Itinerary_Id)
);

CREATE TABLE Notification (
    Notification_Id INT AUTO_INCREMENT PRIMARY KEY,
    User_Id INT,
    Timestamp DATETIME,
    Type VARCHAR(255),
    Message TEXT,
    FOREIGN KEY (User_Id) REFERENCES User(User_Id)
);

CREATE TABLE Booking (
    Booking_Id INT AUTO_INCREMENT PRIMARY KEY,
    Itinerary_Id INT,
    User_Id INT,
    Payment_Info TEXT,
    Payment_Status VARCHAR(50),
    Booking_Status VARCHAR(50),
    Booking_Date DATE,
    FOREIGN KEY (Itinerary_Id) REFERENCES Itinerary(Itinerary_Id),
    FOREIGN KEY (User_Id) REFERENCES User(User_Id)
);

DELIMITER //

CREATE TRIGGER check_destination_availability
AFTER UPDATE ON Destination
FOR EACH ROW
BEGIN
    IF NEW.Availability = TRUE AND OLD.Availability = FALSE THEN
        -- Insert a notification for each user who has this destination in their preferences
        INSERT INTO Notification (User_Id, Timestamp, Type, Message, Destination_Id)
        SELECT 
            up.User_Id, 
            NOW(), 
            'Destination Available', 
            CONCAT('Your preferred destination ', NEW.Name, ' is now available!'),
            NEW.Destination_Id
        FROM 
            UserPreferences up
        WHERE 
            up.Preferences = NEW.Destination_Id;
    END IF;
END //

DELIMITER ;
