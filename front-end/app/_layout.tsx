import {Stack} from 'expo-router';
import {Provider} from "react-redux";
import {store} from "./redux/store";

export default function Layout() {
  return (
      <Provider store={store}>
          <Stack>
              <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
          </Stack>
      </Provider>
  );
}


// import {Tabs} from "expo-router";


// export default function TabLayout(){
//   return (
//     <Tabs>
//       <Tabs.Screen name="HomeScreen" options={{title: "Home"}} />
//       <Tabs.Screen name="MapScreen" options={{title: "Map"}} />
//     </Tabs>
//   )
// }
