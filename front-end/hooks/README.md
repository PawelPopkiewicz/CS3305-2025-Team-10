## getStops()

- called in the map.tsx to display bus stops on the map
- returns

```json
    [
  {
    "id": 1,
    "code": "2232",
    "name": "Patrick Street",
    "lat": -51.1242,
    "lon": 43.1242
  },
  {
    "id": 2,
    "code": "2232",
    "name": "Patrick Street",
    "lat": -51.1242,
    "lon": 43.1242
  },
  "..."
]
```

#### Parameters:

- stop.id(int): unique identifier of the bus stop
- stop.name(str): name of the bus stop, human-readable
- stop.lat, stop.lon(float): latitude and longitude of the bus stop, used to locate it on the map

## getArrivingBuses(stop.id)

- called in [stopId].tsx when users clicks on the bus stop on the map. When clicked, stop.id of selected bus stop is passed to the page, which is then extracted and used to call getStop(stop.id)
- returns

```json

[
  {
    "id": 1,
    "route": "220",
    "headsign": "MTU",
    "arrival": "14:44"
  },
  {
    "id": 2,
    "route": "220X",
    "headsign": "MTU",
    "arrival": "14:44"
  },
  "..."
]

```

#### Parameters:

contains:

- bus.id(int): trip identifier
- bus.route(str): number of the bus (i.e. 220)
- bus.headsign(str): trip destination (i.e MTU)
- bus.arrival(str): predicted arrival time for bus.id

## getBuses()

- called in the map.tsx to display all buses on the map
- returns

```json
[
  {
    "id": 1,
    "route": "220",
    "headsign": "MTU",
    "direction": "25deg",
    "lat": -51.1242,
    "bus.lon": 43.1242
  },
  {
    "id": 2,
    "route": "220",
    "headsign": "MTU",
    "direction": "25deg",
    "lat": -51.1242,
    "bus.lon": 43.1242
  },
  "..."
]
```

#### Parameters:

- bus.id(int): trip identifier
- bus.route(str): number of the bus (i.e. 220)
- bus.headsign(str): trip destination (i.e MTU)
- bus.direction(str): an angle of inclination from top Y-axis to point to direction of movement (degrees + 'deg')
- bus.lon, bus.lat(float): longitude and latitude to display movement of the bus

## getTripInfo(bus.id)

- called in bus.tsx when users clicks on the bus on the map. When clicked, bus.id of selected bus is passed to the page, which is then extracted and used to call getBus(bus.id)
- returns

```json
[
  {
    "id": 1,
    "code": "2232",
    "name": "Patrick Street",
    "arrival": "14:44"
  },
  {
    "id": 2,
    "code": "2232",
    "name": "Patrick Street",
    "arrival": "14:44"
  },
  "..."
]
```

#### Parameters:

list of bus stop that this bus is visiting, (probably including the once already visited?), contains:

- stop.id(int): unique identifier of the bus stop
- stop.name(str): name of the bus stop, human-readable
- stop.arrival(str): predicted arrival time to this bus stop
