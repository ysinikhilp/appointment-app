from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/appointments', methods=['GET'])
def get_appointments():
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("SELECT * FROM appointments")
    rows = c.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1], "date": r[2], "time": r[3]} for r in rows])

@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)",
              (data['name'], data['date'], data['time']))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id, **data})

@app.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    conn = sqlite3.connect('appointments.db')
    c = conn.cursor()
    c.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
    conn.commit()
    deleted = c.rowcount
    conn.close()
    return jsonify({"deleted": deleted})

if __name__ == "__main__":
    app.run(debug=True)