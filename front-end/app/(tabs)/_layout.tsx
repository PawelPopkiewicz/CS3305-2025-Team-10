import FontAwesome from '@expo/vector-icons/FontAwesome';
import {Tabs} from 'expo-router';

export default function TabLayout() {
    return (
        <Tabs screenOptions={{tabBarActiveTintColor: 'blue', headerShown: false}}>
            <Tabs.Screen
                name="index"
                options={{
                    tabBarIcon: ({color}) => <FontAwesome size={28} name="home" color={color}/>,
                }}
            />
            <Tabs.Screen
                name="map"
                options={{
                    tabBarIcon: ({color}) => <FontAwesome size={28} name="map" color={color}/>,
                }}
            />
        </Tabs>
    );
}
