import {createSlice} from "@reduxjs/toolkit";

const busSlice = createSlice({
    name: "bus",
    initialState: {
        busStops: [],  // Static stops (loaded once)
        busRoutes: [], // Updated every 20s
        busPositions: []
    },
    reducers: {
        setBusStops: (state , action) => {
            state.busStops = action.payload;
        },
        setLiveBuses: (state, action) => {
            state.busRoutes = action.payload;
        },
        setBusPositions: (state, action) => {
            state.busPositions = action.payload;
        }
    },
});

export const { setBusStops, setLiveBuses, setBusPositions} = busSlice.actions;
export default busSlice.reducer;
