import {Stack} from 'expo-router';
import {Provider} from "react-redux";
import {store} from "./redux/store";
import {rehydrateFavorites} from "@/app/redux/favSlice";
import {useEffect} from "react";

export default function Layout() {
    useEffect(() => {
        const loadFavorites = async () => {
            await rehydrateFavorites(store.dispatch); // Rehydrate the favorites
        };

        // Return the promise from `loadFavorites` to handle it explicitly
        loadFavorites().catch(error => console.error('Favourite rehydration error:', error));
    }, []);


    return (
      <Provider store={store}>
          <Stack
              screenOptions={{headerShown: false}}>
              <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
          </Stack>
      </Provider>
  );
}
