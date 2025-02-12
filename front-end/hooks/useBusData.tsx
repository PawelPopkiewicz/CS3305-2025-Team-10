import {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {setBusPositions, setBusStops, setLiveBuses} from "@/app/redux/busSlice";
import {RootState} from "@/app/redux/store";
import {busApiUrl} from "@/config/constants";

export const useBusData = () => {
    const dispatch = useDispatch();

    // Select Redux state (so components can use this hook)
    const stops = useSelector((state: RootState) => state.bus.busStops);
    const busRoutes = useSelector((state: RootState) => state.bus.busRoutes);
    const busPositions = useSelector((state: RootState) => state.bus.busPositions);

    useEffect(() => {
        const fetchInitialData = async () => {
            try {
                const stopsData = await fetch(`${busApiUrl}/stops`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }).then((res) => res.json());
                const routesData = await fetch(`${busApiUrl}/routes`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }).then((res) => res.json());

                dispatch(setBusStops(stopsData)); // Store in Redux
                dispatch(setLiveBuses(routesData));
            } catch (error) {
                console.error("Error fetching initial bus data:", error);
            }
        };

        fetchInitialData();

        // Poll live bus positions
        const interval = setInterval(async () => {
            try {
                const positionsData = await fetch(`${busApiUrl}/positions`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }).then((res) => res.json());
                dispatch(setBusPositions(positionsData)); // Store live bus positions in Redux
            } catch (error) {
                console.error("Error fetching live bus positions:", error);
            }
        }, 5000);

        return () => clearInterval(interval); // Cleanup interval on unmount
    }, [dispatch]);

    return { stops, busRoutes, busPositions }; // Other components can access Redux state via this hook
};
