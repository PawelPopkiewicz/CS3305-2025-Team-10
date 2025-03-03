import {Stop} from "@/types/stop";
import {createSlice} from "@reduxjs/toolkit";

interface StopState {
    stops: Stop[];
}

const initialState: StopState = {
    stops: [],
};

export const stopSlice = createSlice({
    name: 'stops',
    initialState,
    reducers: {
        setStops: (state, action) => {
            state.stops = action.payload;
        }
    }
});

export const {setStops} = stopSlice.actions;
export default stopSlice.reducer;
