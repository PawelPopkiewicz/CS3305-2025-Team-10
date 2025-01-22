# Branches
- DBMS
- AI/Model
- Front End
- Benchmarking
- Back End (bus model, account management, client handling)
- Main

# Predictions
- Cancellations
- For next bus route (after terminus)
- Arrival time
- Journey time
- Error checking predictions
- Average actual schedule

# Use Cases
## See the next bus
*Actor*: Passenger
**Main Flow**:
1. Log in the Passenger
2. Passenger chooses the bus route
3. Passenger chooses the bus stop
4. System executes the query for the tuple (route, stop)
5. App displays the information about the next bus coming to this stop on the main page
**Extensions**
1. a: Passenger already logged in once, so the app logs him in automatically (no time outs)
1. b: Passenger needs to confirm cookies and settings (sharing locations, etc.)
2. a: Passenger already picked the favourite bus route, so it is automatically chosen on the home page
3. a: Passenger already picked the favourite bus stop, so if combined with 2a, it displays data on opening the app
5. a: App displays the next few buses coming to this bus stop, instead of just one bus

## Time from bus stop A to bus stop B
*Actor*: Passenger
**Main Flow**:
1. Log in the Passenger
2. Passenger goes to the 
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
	
	- Favourites
		- Pick one or more favourite bus stops (there will be like a star or heart button on the bus stop page)
		- On the homepage display a timetable for the favourite bus stop that you are closest to
		- Show the next few (~4) buses departing from that bus stop
	- etc. to be decided later
- Map
	- Pick a bus stop by clicking on it
	- Search for a bus stop (By id, once found, display the bus stop page (departures from that bus stop))
	- Search for a bus route (like 220 -> displays all 220s currently on the map) -> then you can click on a specific bus on that map which would display the route page
- Bus stop (shows departures)
	- Show the departure from current time
	- Option to specify a later time
	- Option to "heart" it (add it to favourites)
- Route of a bus
	- Show the predictions for a specific bus
	- Display info: name of route, bus id, direction (by terminus station)
	- Option to "heart" it


# Parts
- AI/ML/Predictor
- Client
- Server
- Benchmarking
- Database
