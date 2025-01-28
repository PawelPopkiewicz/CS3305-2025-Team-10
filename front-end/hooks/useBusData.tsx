import { useState, useEffect } from 'react';
import { busApiUrl } from "@/config/constants"

export const useBusData = () => {
    const [busStops, setBusStops] = useState([]);
    const [busRoutes, setBusRoutes] = useState([]);
    const [busPositions, setBusPositions] = useState([]);

    useEffect(() => {
        // Fetch initial data
        fetch(`${busApiUrl}/stops`).then(res => res.json()).then(setBusStops);
        fetch(`${busApiUrl}/routes`).then(res => res.json()).then(setBusRoutes);

        // Poll or use WebSocket for live positions
        const interval = setInterval(() => {
            fetch(`${busApiUrl}/positions`).then(res => res.json()).then(setBusPositions);
        }, 5000);

        return () => clearInterval(interval);
    }, [busApiUrl]);

    return { busStops, busRoutes, busPositions };
};
/* edited ChatGPT, might be revised, fine for a skeleton*/