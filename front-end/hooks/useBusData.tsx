import {useEffect, useRef} from "react";
import {shallowEqual, useDispatch, useSelector} from "react-redux";
import {setBuses} from "@/app/redux/busSlice";
import {setStops} from "@/app/redux/stopSlice";
import {setRoutes} from '@/app/redux/routeSlice';
import {RootState} from "@/app/redux/store";
import {busApiUrl} from "@/config/constants";

let isInitialized = false;

export const useBusData = () => {
    const dispatch = useDispatch();
    const intervalRef = useRef<NodeJS.Timeout | null>(null);
    // Select Redux state
    const stops = useSelector((state: RootState) => state.stop.stops, shallowEqual);
    const buses = useSelector((state: RootState) => state.bus.buses, shallowEqual);
    const routes = useSelector((state: RootState) => state.route.routes, shallowEqual)

    useEffect(() => {
        const fetchStopsData = async () => {
            try {
                const stopsResponse = await fetch(`${busApiUrl}/v1/stops`, {
                    method: "GET",
                    headers: {"Content-Type": "application/json"},
                });

                if (!stopsResponse.ok) {
                    throw new Error("Failed to fetch stops data");
                }

                const stopsData = await stopsResponse.json();
                dispatch(setStops(stopsData));
            } catch (error) {
                console.error("Error fetching stops data:", error);
            }
        };


        const fetchRoutesData = async () => {
            try {
                const routesResponse = await fetch(`${busApiUrl}/v1/routes`, {
                    method: 'GET',
                    headers: {'Content-Type': 'application/json'},
                });

                if (!routesResponse.ok) {
                    throw new Error('Failed to fetch routes data');
                }

                const routesData = await routesResponse.json();
                dispatch(setRoutes(routesData));
            } catch (error) {
                console.error('Error fetching routes data:', error);
            }
        };

        const fetchBusPositions = async () => {
            try {
                const response = await fetch(`${busApiUrl}/v1/buses`, {
                    method: "GET",
                    headers: {"Content-Type": "application/json"},
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const busData = await response.json();
                dispatch(setBuses(busData));
            } catch (error) {
                console.error("Error fetching live bus positions:", error);
            }
        };

        // Only fetch stops data once across the entire app
        if (!isInitialized) {
            fetchStopsData();
            fetchRoutesData();
            isInitialized = true;
        }

        // Always fetch initial bus positions when component mounts
        fetchBusPositions();

        // Only set up the interval if it doesn't exist yet
        if (!intervalRef.current) {
            intervalRef.current = setInterval(fetchBusPositions, 180000);
        }

        // Cleanup function
        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        };
    }, [dispatch]);

    return { stops, buses, routes };
};