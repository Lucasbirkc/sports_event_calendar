# sports_event_calendar
A very simple Backend for a Sports Event Calendar system

## File structure
sports_event_calendar/  <br />
├── database.py         <br />
├── server.py           <br />
├── events.sql          <br />
├── README.md           <br />
├── LICENSE             <br />
└── .gitignore          <br />

## Setup & Run
### 1. Requirements
- Python 3.8 or later (No external libraries required)

### 2. Start the server
Run following in terminal
```
python server.py
```

You should see:
```
Server on http://localhost:8080
```

### 3. Open the application
Visit http://localhost:8080 in your browser

## Project structure
- database.py is SQLite database helper, handling DB connection and queries (Sets up events.db automatically)
- server.py is a simple backend server serving the index.html and API for requests
- index.html is a simple frontend page showing multiple things. The next event, the upcomming week with the events of each day, and a form for adding new events.
- events.db Auto-created SQLite database

## API Overview
| Endpoint       | Method | Description                           |
| -------------- | ------ | ------------------------------------- |
| `/`            | GET    | Serves the main webpage               |
| `/event/next`  | GET    | Returns the next upcoming event       |
| `/events/week` | GET    | Returns all events in the next 7 days |
| `/event`       | POST   | Adds a new event                      |