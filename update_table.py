from flask import Flask,render_template, request,redirect,url_for, flash, abort
import sqlite3 as db
from ids import *
import datetime

def update_table(table, id):
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    max_ids = get_max_ids()
    current_values = get_values(table, id)
    global error; error = False

    if table == "orders":
        clientID = int(request.form.get('clientID'))
        castleID = int(request.form.get('castleID'))
        staffID = int(request.form.get('staffID'))
        locationID = int(request.form.get('locationID'))
        paymentID = int(request.form.get('paymentID'))
        daysrenting = int(request.form.get('daysrenting'))
        current_values.pop(5)
        current_values.pop(6)
        if clientID == "" or castleID == "" or staffID == "" or locationID == "" or paymentID == "" or daysrenting == "":
            flash("Please enter a value into ALL fields", "danger")
            error = True
        elif clientID > int(max_ids[0]):
            flash("User inputted an invalid Client ID", "danger")
            error = True
        elif castleID > int(max_ids[1]):
            flash("User inputted an invalid Castle ID", "danger")
            error = True
        elif staffID > int(max_ids[2]):
            flash("User inputted an invalid Staff ID", "danger")
            error = True
        elif locationID > int(max_ids[3]):
            flash("User inputted an invalid Location ID", "danger")
            error = True
        elif paymentID > int(max_ids[4]):
            flash("User inputted an invalid Payment ID", "danger")
            error = True
        elif daysrenting > 31:
            flash("User inputted an invalid amount for days, Maximum - 31", "danger")
            error = True
        else:
            curs.execute(f"SELECT dayprice FROM castles WHERE id={castleID}")
            price = curs.fetchone()[0]
            curs.execute(f"UPDATE orders SET clientID=?, castleID=?, staffID=?, locationID=?, paymentID=?, daysrenting=?, totalcost=? WHERE ID=?;", (clientID, castleID, staffID, locationID, paymentID, daysrenting, float(price)*daysrenting, id ))
    elif table == 'client' or table == 'staff':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        age = int(request.form.get('age'))
        email = request.form.get('email')
        phone = request.form.get('phone')
        housenumber = int(request.form.get('housenumber'))
        streetname = request.form.get('streetname')
        city = request.form.get('city')
        postcode = request.form.get('postcode')
        if table == 'client':
            if age < 18:
                flash("Please enter a Valid age - 18+", "danger")
                error = True
            else:
                curs.execute("UPDATE client SET fname=?, lname=?, age=?, email=?, phone=?, housenumber=?, streetname=?, city=?, postcode=? WHERE ID=?", (fname.capitalize(), lname.capitalize(), age, email, phone, housenumber, streetname, city, postcode, id))
        else:
            jobID = int(request.form.get('jobID'))
            if jobID > max_ids[5]:
                flash("User inputted an invalid Job ID", "danger")
                error = True
            elif age > 100 or age < 18:
                flash("Please enter a Valid age - 18+")
                error = True
            else:
                curs.execute("UPDATE staff SET fname=?, lname=?, age=?, email=?, phone=?, housenumber=?, streetname=?, city=?, postcode=?, jobID=? WHERE ID=?", (fname.capitalize(), lname.capitalize(), age, email, phone, housenumber, streetname, city, postcode, jobID, id,))
    elif table == 'castles':
        name = request.form.get('name')
        type = request.form.get('type')
        colour = request.form.get('colour')
        size = request.form.get('size')
        maxoccupancy = int(request.form.get('maxocc'))
        details = request.form.get('details')
        dayprice = request.form.get('dayprice')
        locationID = int(request.form.get('locationID'))
        if locationID > max_ids[3]:
            flash("Use inputted an invalid location ID", "danger")
            error = True
        else:
            curs.execute("UPDATE castles SET name=?, type=?, colour=?, size=?, maxoccupancy=?, details=?, dayprice=?, locationID=? WHERE ID=?", (name.title(), type.title(), colour.capitalize(), size.capitalize(), maxoccupancy, details, dayprice, locationID, id,))
    elif table == 'payments':
        typeofpayment = request.form.get('typeofpayment')
        if len(typeofpayment) > 50:
            flash("Maximum characters in type of payment is 50 characters", "danger")
            error = True
        else:
            curs.execute("UPDATE payments SET typeofpayment=? WHERE id=?", (typeofpayment, id,))
    elif table == 'sites':
        phone = request.form.get('phone')
        streetnumber = int(request.form.get('streetnumber'))
        streetname = request.form.get('streetname')
        city = request.form.get('city')
        postcode = request.form.get('postcode')
        curs.execute("UPDATE sites SET phone=?, streetnumber=?, streetname=?, city=?, postcode=? WHERE id=?", (phone, streetnumber, streetname, city, postcode, id,))
    elif table == 'roles':
        jobname = request.form.get('jobname')
        levelofaccess = int(request.form.get('levelofaccess'))
        if len(jobname) > 50:
            flash("Maximum number of characters for Job name is 50", "danger")
            error = True
        elif levelofaccess > 5:
            flash("Maximum level of access is 5", "danger")
            error = True
        else:
            curs.execute("UPDATE roles SET jobname=?, levelofaccess=? WHERE id=?", (jobname, levelofaccess, id, ))
    con.commit()
    con.close()

def add_record_to_db(table):
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    max_ids = get_max_ids()

    global error
    error = False

    current_date = datetime.datetime.now()
    current_date = current_date.strftime('%d/%m/%Y')

    if table == "orders":
        clientID = int(request.form.get('clientID'))
        castleID = int(request.form.get('castleID'))
        staffID = int(request.form.get('staffID'))
        locationID = int(request.form.get('locationID'))
        paymentID = int(request.form.get('paymentID'))
        daysrenting = int(request.form.get('daysrenting'))
        if clientID > int(max_ids[0]):
            flash("User inputted an invalid Client ID", "danger")
            error = True
        elif castleID > int(max_ids[1]):
            flash("User inputted an invalid Castle ID", "danger")
            error = True
        elif staffID > int(max_ids[2]):
            flash("User inputted an invalid Staff ID", "danger")
            error = True
        elif locationID > int(max_ids[3]):
            flash("User inputted an invalid Location ID", "danger")
            error = True
        elif paymentID > int(max_ids[4]):
            flash("User inputted an invalid Payment ID", "danger")
            error = True
        elif daysrenting > 31:
            flash("User inputted an invalid amount for days, Maximum - 31", "danger")
            error = True
        else:
            curs.execute(f"SELECT dayprice FROM castles WHERE id={castleID}")
            price = curs.fetchone()[0]
            curs.execute(f"INSERT INTO orders(clientID, castleID, staffID, locationID, paymentID, dateoforder, daysrenting, totalcost) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (int(clientID), int(castleID), int(staffID), int(locationID), int(paymentID), current_date,  int(daysrenting), float(price)*int(daysrenting)))

    elif table == 'client' or table == 'staff':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        age = int(request.form.get('age'))
        email = request.form.get('email')
        phone = request.form.get('phone')
        housenumber = int(request.form.get('housenumber'))
        streetname = request.form.get('streetname')
        city = request.form.get('city')
        postcode = request.form.get('postcode')
        if table == 'client':
            if age < 18:
                flash("Please enter a Valid age - 18+", "danger")
                error = True
            else:
                curs.execute("INSERT INTO client(fname, lname, age, email, phone, housenumber, streetname, city, postcode) VALUES (?,?,?,?,?,?,?,?,?,?)", (fname.capitalize(), lname.capitalize(), age, email, phone, housenumber, streetname, city, postcode))
        else:
            jobID = request.form.get('jobID')
            if jobID > max_ids[5]:
                flash("User inputted an invalid Job ID", "danger")
                error = True
            elif age > 100 or age < 18:
                flash("Please enter a Valid age - 18+")
                error = True
            else:
                curs.execute("INSERT INTO staff(fname, lname, age, email, phone, housenumber, streetname, city, postcode, jobID) VALUES (?,?,?,?,?,?,?,?,?,?)", (fname.capitalize(), lname.capitalize(), age, email, phone, housenumber, streetname, city, postcode, jobID))
    elif table == 'castles':
        name = request.form.get('name')
        type = request.form.get('type')
        colour = request.form.get('colour')
        size = request.form.get('size')
        maxoccupancy = int(request.form.get('maxocc'))
        details = request.form.get('details')
        dayprice = request.form.get('dayprice')
        locationID = int(request.form.get('locationID'))
        if locationID > max_ids[3]:
            flash("Use inputted an invalid location ID", "danger")
            error = True
        else:
            curs.execute("INSERT INTO castles(name, type, colour, size, maxoccupancy, details, dayprice, locationID) VALUES (?,?,?,?,?,?,?,?)", (name.title(), type.title(), colour.capitalize(), size.capitalize(), maxoccupancy, details, str(float(dayprice)), locationID))
    elif table == 'payments':
        typeofpayment = request.form.get('typeofpayment')
        if len(typeofpayment) > 50:
            flash("Maximum characters in type of payment is 50 characters", "danger")
            error = True
        else:
            curs.execute("INSERT INTO payments(typeofpayment) VALUES (?)", (typeofpayment,))
    elif table == 'sites':
        phone = request.form.get('phone')
        streetnumber = int(request.form.get('streetnumber'))
        streetname = request.form.get('streetname')
        city = request.form.get('city')
        postcode = request.form.get('postcode')
        curs.execute("INSERT INTO sites(phone, streetnumber, streetname, city, postcode) VALUES(?,?,?,?,?)", (phone, streetnumber, streetname, city, postcode))
    elif table == 'roles':
        jobname = request.form.get('jobname')
        levelofaccess = int(request.form.get('levelofaccess'))
        if len(jobname) > 50:
            flash("Maximum number of characters for Job name is 50", "danger")
        if levelofaccess > 5:
            flash("Maximum level of access is 5", "danger")
            error = True
        else:
            curs.execute("INSERT INTO roles(jobname, levelofaccess) VALUES (?,?)" , (jobname, levelofaccess))
    con.commit()
    con.close()

def check_error():
    return error
