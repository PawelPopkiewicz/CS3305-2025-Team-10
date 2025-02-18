import {createSlice, Dispatch, ThunkDispatch, UnknownAction} from '@reduxjs/toolkit';
import AsyncStorage from "@react-native-async-storage/async-storage";
//something up with never[], need to figure out how ts works
const favoritesSlice = createSlice({
    name: 'favorites',
    initialState:
        {
            favStops: [],
            favRoutes: [],
        },
    reducers: {
        addFavoriteStop: (state, action) => {
            // @ts-ignore
            state.favStops.push(action.payload);
        },
        removeFavoriteStop: (state, action) => {
            state.favStops = state.favStops.filter((item) => item !== action.payload);
        },
        setFavoriteStops: (state, action) => {
            return action.payload;
        },
    },
});

export const rehydrateFavorites = async (dispatch: ThunkDispatch<any, any, any> & Dispatch<UnknownAction>) => {
    try {
        const storedFavorites = await AsyncStorage.getItem('favorites');
        if (storedFavorites) {
            dispatch(setFavoriteStops(JSON.parse(storedFavorites)));
        }
        return Promise.resolve();
    } catch (error) {
        console.error('Error rehydrating favorites:', error);
        return Promise.reject(error);
    }
};



export const { addFavoriteStop, setFavoriteStops, removeFavoriteStop} = favoritesSlice.actions;
export default favoritesSlice.reducer;
