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
                const stopsData = await fetch(`${busApiUrl}/v1/getStops`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }).then((res) => res.json());
                const busData = await fetch(`${busApiUrl}/v1/getBuses`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }).then((res) => res.json());
                // console.log("fetched data")
                // console.log(stopsData, busData);
                dispatch(setStops(stopsData)); // Store in Redux
                dispatch(setBuses(busData));
            } catch (error) {
                console.error("Error fetching initial bus data:", error);
            }
        };

        fetchInitialData();

        // Poll live bus positions
        const interval = setInterval(async () => {
            try {
                const positionsData = await fetch(`${busApiUrl}/v1/getBuses`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }).then((res) => res.json());
                dispatch(setBuses(positionsData)); // Store live bus positions in Redux
            } catch (error) {
                console.error("Error fetching live bus positions:", error);
            }
        }, 5000);

        return () => clearInterval(interval); // Cleanup interval on unmount
    }, [dispatch]);

    return { stops, buses }; // Other components can access Redux state via this hook
};
