import {createSlice} from "@reduxjs/toolkit";
import {Bus} from "@/types/bus";

interface BusState {
    buses: Bus[];
}

const initialState: BusState = {
    buses: [],
};

export const busSlice = createSlice({
    name: 'buses',
    initialState,
    reducers: {
        setBuses: (state, action) => {
            state.buses = action.payload;
        }
    }
});

export const {setBuses} = busSlice.actions;
export default busSlice.reducer;
