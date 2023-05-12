import sqlite3 as db

def get_max_ids():
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    max_ids = []
    curs.execute(f"SELECT MAX(id) FROM client")
    client_max_id = curs.fetchall(); client_max_id = client_max_id[0][0]
    curs.execute(f"SELECT MAX(id) FROM castles")
    castles_max_id = curs.fetchall(); castles_max_id = castles_max_id[0][0]
    curs.execute(f"SELECT MAX(id) FROM staff")
    staff_max_id = curs.fetchall(); staff_max_id = staff_max_id[0][0]
    curs.execute(f"SELECT MAX(id) FROM sites")
    location_max_id = curs.fetchall(); location_max_id = location_max_id[0][0]
    curs.execute(f"SELECT MAX(id) FROM payments")
    payment_max_id = curs.fetchall(); payment_max_id = payment_max_id[0][0]
    curs.execute(f"SELECT MAX(id) FROM roles")
    job_max_id = curs.fetchall(); job_max_id = job_max_id[0][0]
    max_ids.append(client_max_id)
    max_ids.append(castles_max_id)
    max_ids.append(staff_max_id)
    max_ids.append(location_max_id)
    max_ids.append(payment_max_id)
    max_ids.append(job_max_id)
    return max_ids

def get_values(table, id):
    con = db.connect("CantyRentalDB.db")
    curs = con.cursor()
    curs.execute(f"SELECT * from {table} where id={id}")
    current_value = curs.fetchone()
    current_value = list(current_value)
    current_value.pop(0)
    return current_value


