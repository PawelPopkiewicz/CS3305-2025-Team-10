import {createSlice, Dispatch, ThunkDispatch} from '@reduxjs/toolkit';
import AsyncStorage from "@react-native-async-storage/async-storage";

interface FavState {
    stops: string[];
    routes: string[];
}

const initialState: FavState = {
    stops: [],
    routes: [],
};

const favoritesSlice = createSlice({
    name: 'favorites',
    initialState,
    reducers: {
        addFavoriteStop: (state, action) => {
            state.stops.push(action.payload);
        },
        removeFavoriteStop: (state, action) => {
            state.stops = state.stops.filter((item) => item !== action.payload);
        },
        setFavoriteStops: (state, action) => {
            return action.payload;
        },
        addFavoriteRoute: (state, action) => {
            state.routes.push(action.payload);
        },
        removeFavoriteRoute: (state, action) => {
            state.routes = state.routes.filter((item) => item !== action.payload);
        },
        setFavoriteRoutes: (state, action) => {
            state.routes = action.payload;
        }
    },
});

export const rehydrateFavorites = async (dispatch: ThunkDispatch<any, any, any> & Dispatch) => {
    try {
        const storedFavorites = await AsyncStorage.getItem('favorites');
        if (storedFavorites) {
            console.log(storedFavorites);
            dispatch(setFavoriteStops(JSON.parse(storedFavorites)));
            dispatch(setFavoriteRoutes(JSON.parse(storedFavorites)));
        }
        return Promise.resolve();
    } catch (error) {
        console.error('Error rehydrating favorites:', error);
        return Promise.reject(error);
    }
};


export const {
    addFavoriteStop,
    setFavoriteStops,
    removeFavoriteStop,
    removeFavoriteRoute,
    setFavoriteRoutes,
    addFavoriteRoute
} = favoritesSlice.actions;
export default favoritesSlice.reducer;
