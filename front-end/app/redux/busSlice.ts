import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {Bus} from "@/types/bus";
import {Stop} from "@/types/stop";

interface BusState {
    stops: Stop[];
    buses: Bus[];
}

const initialState: BusState = {
    stops: [],
    buses: [],
};

const busSlice = createSlice({
    name: "bus",
    initialState,
    reducers: {
        setStops: (state, action: PayloadAction<Stop[]>) => {
            state.stops = action.payload;
        },
        setBuses: (state, action: PayloadAction<Bus[]>) => {
            state.buses = action.payload;
        },
    },
});

export const {setStops, setBuses} = busSlice.actions;
export default busSlice.reducer;
