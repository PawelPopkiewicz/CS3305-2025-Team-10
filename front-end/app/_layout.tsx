import { Stack } from 'expo-router';

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
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
