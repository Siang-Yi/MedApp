import sqlite3

class Database:
    def __init__(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                name TEXT NOT NULL,
                ic TEXT PRIMARY KEY,
                phone_number TEXT,
                address TEXT
            );  
        """)

        conn.commit()
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS history (
                date TEXT NOT NULL,
                symptom TEXT,
                medicine TEXT,
                note TEXT,
                ic TEXT NOT NULL,
                FOREIGN KEY(ic) REFERENCES customer(ic)
            );           
        """)

        conn.commit()
        c.close()
        conn.close()

    def insert_customer(self, customer):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO customer (ic, name, phone_number, address) VALUES (?, ?, ?, ?);  
         """, (customer.ic, customer.name, customer.phone_number, customer.address))
        conn.commit()
        c.close()
        conn.close()

    def get_all_customer(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                    SELECT * FROM customer;  
                 """)
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def get_customer(self, ic):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                    SELECT * FROM customer WHERE ic = ?;  
                 """, (ic,))
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def search_customer(self, keyword):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                            SELECT * FROM customer WHERE name LIKE %s;  
                         """ % ("'" + keyword + "%'"))
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def delete_customer(self, ic):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                            DELETE FROM customer WHERE ic=?;  
                         """, (ic,))
        c.execute("""
                            DELETE FROM history WHERE ic=?;  
                         """, (ic,))
        conn.commit()
        c.close()
        conn.close()

    def edit_customer(self, customer):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                            UPDATE customer SET name = ?, ic = ?, phone_number = ?, address = ? WHERE ic = ?  
                         """, (customer.name, customer.ic, customer.phone_number, customer.address, customer.ic))
        conn.commit()
        c.close()
        conn.close()

    def get_customer_history(self, ic):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                            SELECT rowid, * FROM history WHERE ic=?;  
                         """, (ic,))
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def insert_history(self, history):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                    INSERT INTO history (date, symptom, medicine, note, ic) VALUES (?, ?, ?, ?, ?);  
                 """, (history.date, history.symptom, history.medicine, history.note, history.ic))
        conn.commit()
        c.close()
        conn.close()

    def get_history(self, rowid):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                            SELECT rowid, * FROM history WHERE rowid=?;
                         """, (rowid,))
        data = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return data

    def edit_history(self, history, rowid):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                            UPDATE history SET date = ?, symptom = ?, medicine = ?, note = ? WHERE rowid = ?  
                         """, (history.date, history.symptom, history.medicine, history.note, rowid))
        conn.commit()
        c.close()
        conn.close()

    def delete_history(self, rowid):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("""
                            DELETE FROM history WHERE rowid=?;  
                         """, (rowid,))
        conn.commit()
        c.close()
        conn.close()


if __name__ == "__main__":
    database = Database()

