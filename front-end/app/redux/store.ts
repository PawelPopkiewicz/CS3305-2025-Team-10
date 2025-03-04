import {configureStore} from "@reduxjs/toolkit";
import busReducer from "./busSlice";
import favReducer from "./favSlice";
import stopReducer from "./stopSlice";
import routeSlice from "./routeSlice";
import AsyncStorage from '@react-native-async-storage/async-storage';

export const store = configureStore({
    reducer: {
        bus: busReducer,
        route: routeSlice,
        stop: stopReducer,
        fav: favReducer,
    },
});

store.subscribe(async () => {
    const state = store.getState();
    try {
        await AsyncStorage.setItem('favorites', JSON.stringify(state.fav));
    } catch (error) {
        console.error('Error saving favorites:', error);
    }
});

export type RootState = ReturnType<typeof store.getState>;
export default store;