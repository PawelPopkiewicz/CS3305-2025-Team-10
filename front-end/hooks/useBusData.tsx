import {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {setBuses, setStops} from "@/app/redux/busSlice";
import {RootState} from "@/app/redux/store";
import {busApiUrl} from "@/config/constants";

export const useBusData = () => {
    const dispatch = useDispatch();

    // Select Redux state (so components can use this hook)
    const stops = useSelector((state: RootState) => state.bus.stops);
    const buses = useSelector((state: RootState) => state.bus.buses);

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const [stopsResponse, busResponse] = await Promise.all([
                    fetch(`${busApiUrl}/v1/stops`, {
                        method: "GET",
                        headers: {"Content-Type": "application/json"},
                    }),
                    fetch(`${busApiUrl}/v1/buses`, {
                        method: "GET",
                        headers: {"Content-Type": "application/json"},
                    }),
                ]);

                if (!stopsResponse.ok || !busResponse.ok) {
                    throw new Error("Failed to fetch data");
                }

                const [stopsData, busData] = await Promise.all([
                    stopsResponse.json(),
                    busResponse.json(),
                ]);

                dispatch(setStops(stopsData)); // Store in Redux
                dispatch(setBuses(busData));

            } catch (error) {
                console.error("Error fetching initial bus data:", error);
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
                dispatch(setBuses(busData)); // Store live bus positions in Redux
            } catch (error) {
                console.error("Error fetching live bus positions:", error);
            }
        };

        fetchInitialData();
        fetchBusPositions();

        const interval = setInterval(fetchBusPositions, 5000);

        return () => clearInterval(interval);
    }, [dispatch]);

    return { stops, buses }; // Other components can access Redux state via this hook
};
