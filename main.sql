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

CREATE PROCEDURE AddBooking(
    IN itinerary_id INT,
    IN user_id INT,
    IN payment_status VARCHAR(50),
    IN booking_status VARCHAR(50),
    IN booking_date DATE
)
BEGIN
    DECLARE payment_info TEXT DEFAULT 'Paid through portal';

    -- Insert booking data into the Booking table
    INSERT INTO Booking (Itinerary_Id, User_Id, Payment_Info, Payment_Status, Booking_Status, Booking_Date)
    VALUES (itinerary_id, user_id, payment_info, payment_status, booking_status, booking_date);
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER check_destination_availability
AFTER UPDATE ON Destination
FOR EACH ROW
BEGIN
    IF NEW.Availability = 1 AND OLD.Availability = 0 THEN
        INSERT INTO Notification (User_Id, Timestamp, Type, Message)
        SELECT 
            up.User_Id, 
            NOW(), 
            'Destination Available', 
            CONCAT('Your preferred destination ', NEW.Name, ' is now available!')
        FROM 
            UserPreferences up
        WHERE 
            up.Preferences = NEW.Destination_Id;
    END IF;
END //

DELIMITER ;


'''
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

CREATE PROCEDURE AddBooking(IN itinerary_id INT,
    IN user_id INT,
    IN payment_status VARCHAR(50),
    IN booking_status VARCHAR(50),
    IN booking_date DATE
)
BEGIN
    DECLARE payment_info TEXT DEFAULT 'Paid through portal';

    -- Insert booking data into the Booking table
    INSERT INTO Booking (Itinerary_Id, User_Id, Payment_Info, Payment_Status, Booking_Status, Booking_Date)
    VALUES (itinerary_id, user_id, payment_info, payment_status, booking_status, booking_date);
END ;

DELIMITER //
SHOW PROCEDURE STATUS WHERE Db = 'travelplanner' AND Name = 'AddBooking';


DELIMITER $$

CREATE TRIGGER check_destination_availability
AFTER UPDATE ON Destination
FOR EACH ROW
BEGIN
    IF NEW.Availability = 1 AND OLD.Availability = 0 THEN
        INSERT INTO Notification (User_Id, Timestamp, Type, Message)
        SELECT 
            up.User_Id, 
            NOW(), 
            'Destination Available', 
            CONCAT('Your preferred destination ', NEW.Name, ' is now available!')
        FROM 
            UserPreferences up
        WHERE 
            up.Preferences = NEW.Destination_Id;
    END IF;
END $$

DELIMITER ;
select * from user;
select * from booking;

select * from UserPreferences;
select * from notification;

select * from itinerary;
UPDATE Destination SET Availability = 0 WHERE Destination_Id = 9;
select * from destination;
select * from notification;
select * from userpreferences;
select * from booking;
select * from user;
'''