import sqlite3

def init_db():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            dealer_name TEXT NOT NULL,
            company TEXT NOT NULL,
            vehicle_name TEXT NOT NULL,
            odometer_reading INTEGER NOT NULL,
            sale_date TEXT NOT NULL,
            dealer_address TEXT NOT NULL,
            city TEXT NOT NULL,
            image_url TEXT NOT NULL,
            infotainment_serial_no TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def store_complaint(complaint_id, dealer_name, company, vehicle_name, odometer_reading, sale_date, dealer_address, city, image_url, infotainment_serial_no):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO complaints (complaint_id, dealer_name, company, vehicle_name, odometer_reading, sale_date, dealer_address, city, image_url, infotainment_serial_no)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (complaint_id, dealer_name, company, vehicle_name, odometer_reading, sale_date, dealer_address, city, image_url, infotainment_serial_no))
    conn.commit()
    conn.close()

def check_infotaiment_serial(serial_no):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('SELECT complaint_id FROM complaints WHERE infotainment_serial_no = ?', (serial_no,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def get_complaint_by_id(complaint_id):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM complaints WHERE complaint_id = ?', (complaint_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'complaint_id': row[0],
            'dealer_name': row[1],
            'company': row[2],
            'vehicle_name': row[3],
            'odometer_reading': row[4],
            'sale_date': row[5],
            'dealer_address': row[6],
            'city': row[7],
            'image_url': row[8],
            'infotainment_serial_no': row[9]
        }
    return None
