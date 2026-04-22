import sqlite3

def check_db():
    conn = sqlite3.connect('robot_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM detections')
    rows = cursor.fetchall()

    if not rows:
        print("Database is empty. No detections stored yet.")
    else:
        print("ID | Timestamp | Object Type | Bounding Box | Confidence | Temperature | Radiation | Uploaded")
        print("-" * 100)
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    check_db()