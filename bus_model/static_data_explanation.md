## Trip
A single instance of a vehicle travelling on a route. It is a journey on a specific bus route at a specific time on the schedule. A trip is tied to a specific route. stop_times.txt contains the list of times for each stop (and some additional info) for each trip.

## Stop
A bus stop. It has an internal and external ID, and a location.

## Route
A route is a collection of trips that fall under one name (eg. 220 or 220X). It can have multiple different shape_id associated with the route. This means that every bus on the route does not travel to the same place. (eg. There is one 220X that goes to MTU instead of Ballincollig daily)
The route can branch, and describe both directions of travel.

## Service
A ID that shows the dates where the service runs, when the service is valid from and to, and also known exceptions to the schedule (eg. Christmas)

## Shape
A shape is a sequence of lat/long points that denote where a trip is scheduled to go. This is more detailed than a list of stops. It is directional.

## Structure of the Model
- Many routes
    - Many trips
        - One bus
        - One service (shared by many trips, but can duplicate?)
        - Many stops (shared)
            - One time per stop
        - One shape

Classes
- Routes
- Trips
- Busses
- Services (simple)
- Stops
- Shapes
- Agency (not really useful)
- Bus stop visit (each line of stop_times.txt)

## Parsing Order
As some files have foreign keys, these must be parsed later.
- Agency
- Calendar
- Stops
- Shapes

And then
- Calendar Dates (depends on calendar)
- Routes (depends on agency)

And then
- Trips (depends on shapes, services, routes)

And then
- Stop times (depends on trips, stops)

## Extra
Video for better explanation [here](https://www.youtube.com/watch?v=8OQKHhu1VgQ)

## Scale of the Data (incl new sizes)
- 439 routes            -> 437 routes
- 151k trips            -> 250k trips
- 5mil stop_times       -> 7.1mil stop_times
- 10500 stops           -> 10500 stops
- 4.5mil shape-points   -> 6.4mil shape-points
- Few thousand vehicles -> same

