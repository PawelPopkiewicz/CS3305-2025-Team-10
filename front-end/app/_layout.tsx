import {Stack} from 'expo-router';
import {Provider} from "react-redux";
import {store} from "./redux/store";

export default function Layout() {
  return (
      <Provider store={store}>
          <Stack
              screenOptions={{headerShown: false}}>
              <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
          </Stack>
      </Provider>
  );
}