import {createSlice, Dispatch, ThunkDispatch} from '@reduxjs/toolkit';
import AsyncStorage from "@react-native-async-storage/async-storage";

interface FavState {
    routes: string[];
}

const initialState: FavState = {
    routes: [],
};

const favRoutesSlice = createSlice({
    name: 'favRoutes',
    initialState,
    reducers: {
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

export const rehydrateRoutesFavorites = async (dispatch: ThunkDispatch<any, any, any> & Dispatch) => {
    try {
        const storedFavorites = await AsyncStorage.getItem('favRoutes');
        if (storedFavorites) {
            const parsedFavorites = JSON.parse(storedFavorites);
            const routes = Array.isArray(parsedFavorites.routes) && parsedFavorites.routes.every((item: string) => typeof item === 'string')
                ? parsedFavorites.routes
                : [];
            dispatch(setFavoriteRoutes(routes));
            console.log(routes);
        }
        return Promise.resolve();
    } catch (error) {
        console.error('Error rehydrating favorite routes:', error);
        return Promise.reject(error);
    }
};


export const {
    removeFavoriteRoute,
    setFavoriteRoutes,
    addFavoriteRoute
} = favRoutesSlice.actions;
export default favRoutesSlice.reducer;
