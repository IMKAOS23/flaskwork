from flask import Flask,render_template,request,redirect,url_for,flash, abort
import sqlite3 as db
from ids import *
from update_table import *
import os
from initiatedb import initiatedb

app = Flask(__name__)
app.secret_key = "378412"

if os.path.exists("CantyRentalDB.db"):
    print("CantyRentalDB.db already exists")
else:
    initiatedb()
    print("Successfully created database \"CantyRentalDB.db\"")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        table = request.form.get('table')
        flash(f"Showing values for {table}", category="success")
        return redirect(url_for("show_table", table=table))

    return render_template('home.html')

@app.route('/<table>', methods=['GET', 'POST'])
def show_table(table):
    con = db.connect('CantyRentalDB.db')
    con.row_factory = db.Row
    curs = con.cursor()
    results = curs.execute(f"SELECT * FROM {table}")
    columns = []
    for tuple in results.description:
        columns.append(tuple[0])
    tabledata = curs.fetchall()
    if request.method == 'POST':
        table = request.form.get('table')
        flash(f"Showing values for {table}", category="success")
        return redirect(url_for("show_table", table=table))
    return render_template('table.html', columns=columns, table=table, data=tabledata)

@app.route('/<table>/add', methods=['GET', 'POST'])
def add_record(table):
    max_ids = get_max_ids()
    if request.method == "POST":
        add_record_to_db(table)
        error = check_error()
        if error != True:
            flash(f"Successfully add record to {table}", "success")
            return redirect(url_for("show_table", table=table))
    return render_template('add_record.html', table=table, max_ids=max_ids)

@app.route('/<table>/edit/<id>', methods=['GET', 'POST'])
def edit_record(table, id):
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    result = curs.execute(f"SELECT * FROM {table} WHERE id={id}")
    record = result.fetchone()
    max_ids = get_max_ids()
    current_values = get_values(table, id)
    if table == "orders":
        curs.execute(f"SELECT castleID FROM orders WHERE id={id}")
        castle_id = curs.fetchone()[0]
        curs.execute(f"SELECT daysrenting FROM orders WHERE id={id}")
        days_renting = curs.fetchone()[0]
    if request.method == "POST":
        update_table(table, id)
        error = check_error()
        if error == False:
            flash(f"Successfully editted record with ID:{id} for {table}", "success")
            return redirect(url_for('show_table', table=table))
    if table == "orders":
        return render_template('edit_record.html', table=table, id=id, max_ids=max_ids, current_values=current_values, castle_id=castle_id, days_num=days_renting)
    else:
        return render_template('edit_record.html', table=table, id=id, max_ids=max_ids, current_values=current_values)

@app.route('/<table>/delete/<id>', methods=['GET','POST'])
def delete_record(table, id):
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    curs.execute(f"DELETE FROM {table} WHERE id={id}")
    con.commit()
    con.close()
    flash(f"Successfully deleted record with id-{id} from {table}", "success")
    return redirect(url_for('show_table', table=table))

def total_cost(id, castle_id):
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    curs.execute(f"SELECT dayprice FROM castles WHERE id={castle_id}")
    price = curs.fetchall()
    curs.execute(f"SELECT daysrenting FROM orders WHERE id={id}")
    days = curs.fetchall()
    price = float(price[0][0])
    days = days[0][0]
    return price * days
app.jinja_env.globals.update(total_cost = total_cost)

app.run(debug=True)
