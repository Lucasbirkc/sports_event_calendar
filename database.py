import sqlite3

DB = 'events.db'

def init_db():
    # Connection (Initializing if not exist)
    connection = sqlite3.connect(DB)

    # Cursor for executing SQL statements
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            sport TEXT NOT NULL,
            teams TEXT NOT NULL
        );           
    """)
    # Commit transaction to save changes
    connection.commit()

    # Close connection
    connection.close()

def add_event(date, time, sport, teams, connection):
    # Create cursor for SQL statement execution
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO events (date, time, sport, teams) VALUES (?, ?, ?, ?)
        """,
        (date, time, sport, teams)
    )
    
    # Save transaction and close connection
    connection.commit()
    connection.close()

# Test DB setup and add_event function. Insertion confirmed in Database Client add-on
init_db()
connection = sqlite3.connect(DB)
add_event("22/10/2025", "15:29", "handball", "A vs B", connection)
print("Event added")

