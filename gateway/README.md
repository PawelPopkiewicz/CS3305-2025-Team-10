

## showStops()
- called in the map.tsx to display bus stops on the map
- returns 
```json
{
	stops : 
	[
		{
			id: 1,
			name: "Patrick Street",
			lat: -51.1242,
			lon: 43.1242
		},
		{
			id: 2,
			....
		},
		...
	]
}
```

#### Parameters:
- stop.id - unique identifier of the bus stop
- stop.name - name of the bus stop, human readable
- stop.lat, stop.lon - latitude and longitude of the bus stop, used to locate it on the map

## getArrivingBuses(stop.id)
- called in stop.tsx when users clicks on the bus stop on the map. When clicked, stop.id of selected bus stop is passed to the page, which is then extracted and used to call getStop(stop.id)
- returns

```json
{
	buses : 
	[
		{
			id: 1,
			route: "220",
			headsign: "MTU",
			arrival: "14:44"
		},
		{        
			id: 2,
			route: "220x",
			....
		},
		...
	]
} 

```

#### Parameters:
contains:
    - bus.id - trip identifier
    - bus.route - number of the bus (i.e 220)
    - bus.headsign - trip destination (i.e MTU)
    - bus.arrival - predicted arrival time for bus.id
## showBuses()
- called in the map.tsx to display all buses on the map
- returns 
```json
{
	buses : 
	[
		{
			id: 1,
			route: "220",
			headsign:  "MTU",
			direction: 0
			lat: -51.1242,
			bus.lon: 43.1242
		},
		{
			id: 2,
			....
		},
		...
	]
}
```

#### Parameters:
- bus.id - trip identifier
- bus.route - number of the bus (i.e 220)
- bus.headsign - trip destination (i.e MTU)
- bus.direction - 0 or 1 depending on inbound or outbound travel
- bus.lon, bus.lat - longitude and latitude to display movement of the bus

## getTripInfo(bus.id)
- called in bus.tsx when users clicks on the bus  on the map. When clicked, bus.id of selected bus is passed to the page, which is then extracted and used to call getBus(bus.id)
- returns 

```json
{
	stops :
	[
		{
			id: 1,
			name: "Patrick Street",
			arrival: "14:44"
		},
		{
			id: 2,
			...
		},
		...
	]
}
```

#### Parameters:
list of bus stop that this bus is visiting, (probably including the once already visited?), contains:
    - stop.id - unique identifier of the bus stop
    - stop.name - name of the bus stop, human readable
    - stop.arrival - predicted arrival time to this bus stop
