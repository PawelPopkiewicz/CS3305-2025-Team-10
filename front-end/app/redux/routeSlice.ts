import {Route} from "@/types/route";
import {createSlice} from "@reduxjs/toolkit";

interface RouteState {
    routes: Route[];
}

const initialState: RouteState = {
    routes: [],
};

export const routeSlice = createSlice({
    name: 'routes',
    initialState,
    reducers: {
        setRoutes: (state, action) => {
            state.routes = action.payload;
        }
    }
});

export const {setRoutes} = routeSlice.actions;
export default routeSlice.reducer;
