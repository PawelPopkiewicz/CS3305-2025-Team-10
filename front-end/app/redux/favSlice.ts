import { createSlice, Dispatch, ThunkDispatch, UnknownAction} from '@reduxjs/toolkit';
import AsyncStorage from "@react-native-async-storage/async-storage";

const favoritesSlice = createSlice({
    name: 'favorites',
    initialState:
        {
            favStops: ["aaa"],
            favRoutes: ["aaa"],
        },
    reducers: {
        addFavoriteStop: (state, action) => {
            console.log('State before push:', state.favStops);
            state.favStops.push(action.payload); // Push to the array
            console.log('State after push:', state.favStops);
        },
        removeFavoriteStop: (state, action) => {
            console.log('State before removal:', state.favStops);
            state.favStops = state.favStops.filter((item) => item !== action.payload);
            console.log('State after removal:', state.favStops);
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
