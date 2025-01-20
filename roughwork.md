# Branches
- DBMS
- AI/Model
- Client App
- Benchmarking
- Server (bus model, account management, client handling)

# Predictions
- Cancellations
- For next bus route (after terminus)
- Arrival time
- Journey time
- Error checking predictions
- Average actual schedule

# Use Cases
- Next bus time for 1 route, 1 bus stop
- Show next few buses
- Time from bus stop A to bus stop B
- Bus locations (map)
- Off route/cancelled buses
- Public API

# Responsibilities
(Client)
- Display data
- Calc shortest route to a busstop
- Render map

# Database Storage
- Bus stop data
- Bus schedule
- Bus routes
- Historical data
- User meta-data
- Account info

# Services
(By server)
- AI predictions
- Account management
- Bus info model (routes, steps, timetables, traffic)
- Client request handling

# MVP
- Bus stop sign, in app
- Choose stop, bus route. Return expected time

# Pages
(In app)
- Homepage
- Map
- Bus stop (shows departures)
- Route of a bus

# Parts
- AI/ML/Predictor
- Client
- Server
- Benchmarking
- Database