import {configureStore} from "@reduxjs/toolkit";
import busReducer from "./busSlice";
import favStopReducer from "./favStopsSlice";
import favRouteReducer from "./favRoutesSlice";
import stopReducer from "./stopSlice";
import routeSlice from "./routeSlice";
import AsyncStorage from '@react-native-async-storage/async-storage';

export const store = configureStore({
    reducer: {
        bus: busReducer,
        route: routeSlice,
        stop: stopReducer,
        favStop: favStopReducer,
        favRoute: favRouteReducer,
    },
});

store.subscribe(async () => {
    const state = store.getState();
    try {
        await AsyncStorage.setItem('favStops', JSON.stringify(state.favStop))
        await AsyncStorage.setItem('favRoutes', JSON.stringify(state.favRoute))
    } catch (error) {
        console.error('Error saving favorites:', error);
    }
});

export type RootState = ReturnType<typeof store.getState>;
export default store;