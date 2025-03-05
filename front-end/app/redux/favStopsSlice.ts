import {createSlice, Dispatch, ThunkDispatch} from '@reduxjs/toolkit';
import AsyncStorage from "@react-native-async-storage/async-storage";

interface FavStops {
    stops: string[];
}

const initialState: FavStops = {
    stops: [],
};

const favStopsSlice = createSlice({
    name: 'favStops',
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
        }
    },
});

export const rehydrateStopsFavorites = async (dispatch: ThunkDispatch<any, any, any> & Dispatch) => {
    try {
        const storedFavorites = await AsyncStorage.getItem('favStops');
        if (storedFavorites) {
            const parsedFavorites = JSON.parse(storedFavorites);
            const stops = Array.isArray(parsedFavorites.stops) && parsedFavorites.stops.every((item: string) => typeof item === 'string')
                ? parsedFavorites.stops
                : [];
            dispatch(setFavoriteStops(stops));
            console.log(stops);
        }
        return Promise.resolve();
    } catch (error) {
        console.error('Error rehydrating favorite stops:', error);
        return Promise.reject(error);
    }
};


export const {
    addFavoriteStop,
    setFavoriteStops,
    removeFavoriteStop,
} = favStopsSlice.actions;
export default favStopsSlice.reducer;
