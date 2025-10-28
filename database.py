import sqlite3
from typing import Tuple

DB_PATH = 'events.db'

def event_to_dict(event_tuple: Tuple):
    event_dict = {}
    event_dict['datetime'] = event_tuple[0]
    event_dict['sport'] = event_tuple[1]
    event_dict['teams'] = event_tuple[2]
    return event_dict

class EventDB():
    def __init__(self, db_path='events.db'):
        self.db_path = db_path
        self.connection = None

    # Open database connection and init schema (if necessary)
    def __enter__(self):
        # DB Connection
        self.connection = sqlite3.connect(self.db_path)
        self._init_schema()
        return self
    
    # Clean up connection
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            self.connection = None

    def get_connection(self):
        if not self.connection:
            # TODO: Should this really be RuntimeError?
            raise RuntimeError("DB not connected.")
        return self.connection
    
    def _init_schema(self):
        # Cursor for executing SQL statements
        cursor = self.connection.cursor()

        # Dates and time stored in ISO 8601 format for optimized ordering in queries
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime TEXT NOT NULL,
                sport TEXT NOT NULL,
                teams TEXT NOT NULL
            );           
        """)
        # Commit transaction to save changes
        self.connection.commit()
        

class EventHandler():
    def __init__(self, db):
        self.db = db
        self.connection = db.get_connection()

    def add_event(self, datetime: str, sport: str, teams: str):
        # Create cursor for SQL statement execution
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO events (datetime, sport, teams) VALUES (?, ?, ?)
            """,
            (datetime, sport, teams)
        )
        
        # Save transaction
        self.connection.commit()
        return cursor.lastrowid

    def get_events(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT datetime, sport, teams FROM events
            """
        )
        return cursor.fetchall()
    
    def get_event(self, event_id):
        cursor = self.connection.cursor()
        # TODO: Test this works as intended
        cursor.execute(
            """
            SELECT datetime, sport, teams FROM events WHERE id=?
            """, (event_id,)
        )
        return cursor.fetchone()

    def get_next_event(self):
        cursor = self.connection.cursor()
        # TODO: Test this works as intended
        cursor.execute(
            """
            SELECT datetime, sport, teams FROM events ORDER BY datetime
            """
        )
        return cursor.fetchone()

# Test DB setup and add_event function. Insertion confirmed in Database Client add-on
with EventDB(DB_PATH) as db:
    handler = EventHandler(db)
    # handler.add_event("2025-10-24T11:20:00", "Basketball", "BC vs BD")
    # handler.add_event("2025-10-24T11:25:00", "Handball", "HC vs HD")
    # handler.add_event("2025-10-24T12:25:00", "Football", "FC vs FD")

    # handler.add_event("2025-10-25T11:20:00", "Hockey", "HoC vs HoD")
    # handler.add_event("2025-11-24T11:20:00", "Golf", "Woods")
    # handler.add_event("2025-12-24T11:20:00", "Disc Golf", "DA vs DD")
    # handler.add_event("2026-12-02T11:20:00", "Ice Skating", "IC vs ID")
    # handler.add_event("2027-12-3T11:20:00", "Dance Battle", "DBC vs DBD")

    # print(f"Event 2: {handler.get_event(2)}")
    # print(f"Event 3: {handler.get_event(3)}")
    # print(f"Event 5: {handler.get_event(5)}")
    # print(f"All events: {handler.get_events()}")

    print(f"Next Event: {handler.get_next_event()}")

# add_event("22/10/2025", "15:29", "handball", "A vs B", connection)
# print("Event added")

