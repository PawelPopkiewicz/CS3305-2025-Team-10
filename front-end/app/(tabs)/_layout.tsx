import FontAwesome from '@expo/vector-icons/FontAwesome';
import {Tabs} from 'expo-router';

import colors from "@/config/Colors";
import fonts from "@/config/Fonts";

export default function TabLayout() {
    return (
        <Tabs screenOptions={{tabBarActiveTintColor: colors.objectSelected, headerShown: false, 
        tabBarStyle:{backgroundColor:colors.backgroundPrimary},
        tabBarLabelStyle:{fontSize:fonts.body},
        }}>
            
            <Tabs.Screen
                name="index"
                options={{
                    title:"Home",
                    tabBarIcon: ({color}) => <FontAwesome size={28} name="home" color={color}/>,
                }}
            />
            <Tabs.Screen
                name="map"
                options={{
                    title:"Map",
                    tabBarIcon: ({color}) => <FontAwesome size={28} name="map" color={color}/>,
                }}
            />
            
        </Tabs>
    );
}

