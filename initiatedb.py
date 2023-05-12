import sqlite3 as db

def initiatedb():
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    curs.executescript('''
CREATE TABLE IF NOT EXISTS "client" ("ID" INTEGER UNIQUE,"fname" TEXT,"lname" TEXT,"age" INTEGER,"email" TEXT,"phone" NUMERIC,"housenumber" INTEGER,"streetname" TEXT,"city" TEXT,"postcode" TEXT,PRIMARY KEY("ID" AUTOINCREMENT));
CREATE TABLE IF NOT EXISTS "staff" ("ID" INTEGER UNIQUE, "fname" TEXT, "lname" TEXT,"age" INTEGER,"email" TEXT,"phone" NUMERIC,"housenumber" INTEGER, "streetname" TEXT,"city" TEXT,"postcode" TEXT,"jobID" INTEGER,FOREIGN KEY("jobID") REFERENCES "roles"("ID"), PRIMARY KEY("ID" AUTOINCREMENT));
CREATE TABLE IF NOT EXISTS "castles" ("ID" INTEGER UNIQUE, "name" TEXT, "type" TEXT, "colour" TEXT, "size" TEXT, "maxoccupancy" INTEGER,"details" TEXT,"dayprice" REAL,"locationID" INTEGER, FOREIGN KEY("locationID") REFERENCES "sites"("id"),PRIMARY KEY("ID" AUTOINCREMENT));
CREATE TABLE IF NOT EXISTS "sites" ("ID" INTEGER UNIQUE, "phone" TEXT,"streetnumber" INTEGER,"streetname" TEXT,"city" TEXT,"postcode" TEXT,PRIMARY KEY("ID" AUTOINCREMENT));
CREATE TABLE IF NOT EXISTS "roles" ("ID" INTEGER UNIQUE, "jobname" TEXT, "levelofaccess" INTEGER,PRIMARY KEY("ID" AUTOINCREMENT));
CREATE TABLE IF NOT EXISTS "payments" ("ID" INTEGER UNIQUE, "typeofpayment" TEXT,PRIMARY KEY("ID" AUTOINCREMENT));
CREATE TABLE IF NOT EXISTS "orders" ("ID" INTEGER UNIQUE, "clientID" INTEGER, "castleID" INTEGER, "staffID" INTEGER, "locationID" INTEGER, "paymentID" INTEGER, "dateoforder" TEXT, "daysrenting" INTEGER,"totalcost"	TEXT,FOREIGN KEY("paymentID") REFERENCES "payments"("ID"),FOREIGN KEY("locationID") REFERENCES "sites"("ID"), FOREIGN KEY("castleID") REFERENCES "castles"("ID"), FOREIGN KEY("clientID") REFERENCES "client"("ID"), FOREIGN KEY("staffID") REFERENCES "staff"("ID"), PRIMARY KEY("ID" AUTOINCREMENT));
    ''')

    # Adding a single value to each of the tables

    curs.execute("INSERT INTO client (fname, lname, age, email, phone, housenumber, streetname, city, postcode) VALUES ('Mark', 'Canty', 20, 'markcanty0123@example.com', 07340777432, 80, 'South Street', 'Manchester', 'M11 4QV')")
    curs.execute("INSERT INTO roles (jobname, levelofaccess) VALUES ('CustomerService', 3)")
    curs.execute("INSERT INTO sites (phone, streetnumber, streetname, city, postcode) VALUES (07456327923, 456, 'West Avenue', 'Manchester', 'M11 4VP')")
    curs.execute("INSERT INTO payments (typeofpayment) VALUES ('Card')")
    curs.execute("INSERT INTO staff (fname, lname, age, email, phone, housenumber, streetname, city, postcode, jobID) VALUES ('Steve', 'Hopkins', 33, 'stevehopkins@example.com', 07567321098, 73, 'Keynsham Road', 'Manchester', 'M11 4HX', 1)")
    curs.execute("INSERT INTO castles (name, type, colour, size, maxoccupancy, details, dayprice, locationID) VALUES ('Sea Breeze Obsticle Course', 'Inflatable Obsticle Course', 'Blue', 'Large', 12, 'Good condition, requires a large pump to be ran due to the size.', 125.0, 1)")
    curs.execute("INSERT INTO castles (name, type, colour, size, maxoccupancy, details, dayprice, locationID) VALUES ('Waterway Slip N Slide', 'Inflatable Waterslide', 'Lime', 'Medium', 8, '15-meter-long inflatable slip and slide. Overall condition is Good, with no signs of malfunction.', 75.0 , 1)")
    curs.execute("INSERT INTO Orders (clientID, castleID, staffID, locationID, paymentID, dateoforder, daysrenting, totalcost) VALUES (1, 2, 1, 1, 1, '20/01/2023', 5, 375.0)")
    con.commit()
    con.close()
