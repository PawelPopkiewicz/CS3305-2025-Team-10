import {Platform, SafeAreaView, StyleSheet, Text, View, StatusBar} from "react-native";
import {Button, Icon} from 'react-native-elements';
import {router, useLocalSearchParams} from 'expo-router';
import { ScrollView } from "react-native";

import colors from "@/config/Colors";
import fonts from "@/config/Fonts";


const TripInfo = ({ bus }) => (

    // Display each stop of the selected bus ordered by arrival time
    <ScrollView style={styles.path}>

        {/* component for each stop */}
        {bus.map((busStop) => (

            <View key={busStop.id} style={styles.stop}>
                <View style={styles.first}>
                    <Icon iconStyle={styles.busPathVisited} name="arrow-down" type="font-awesome"/>
                </View>
                <View style={styles.second}>
                    <Text style={styles.textSecondary}>{`Stop ${busStop.code} ${busStop.name}`}</Text>      {/* Stop info i.e. Stop 223 University College Cork */}
                </View>
                <View style={styles.third}>
                    <Text style={styles.time}>{busStop.arrival}</Text>      {/* arrival time */}
                </View>
            </View>

        ))}
    </ScrollView>
);

export default function Bus() {

        const params = useLocalSearchParams();
        const bus = params.bus ? JSON.parse(params.bus) : [];

        // const bus = [
        //     { id: 1, code: '2232', name: 'University College, Cork', arrival: '14:32' },
        //     { id: 2, code: '7890', name: 'City Centre, Cork', arrival: '15:45' },
        //     { id: 3, code: '4567', name: 'Kent Station, Cork', arrival: '15:00' }
        // ]

        const sortedBus = [...bus].sort((a, b) => {
            return a.arrival.localeCompare(b.arrival);
        });

return (
    <SafeAreaView
        style={styles.background}
    >
        {/* Chosen bus */}
        <View style={styles.bus}>
            <Button
                icon={<Icon iconStyle={styles.icon} name="chevron-left" type="font-awesome"/>}
                buttonStyle={styles.button}     // go back button
                onPress={() => router.back()}
                >
            </Button>

            <View style={styles.route}>
                <Text style={styles.textPrimary}>220</Text>     {/*bus route */}
            </View>

            <View style={styles.heading}>
                <Text style={styles.textPrimary}>Carrigaline-Crosshaven</Text>  {/*bus headsign */}
            </View>

            {/* to be made functional once we store favourites */}
            <Button                
                icon={<Icon iconStyle={styles.icon} name="star" type="font-awesome"/>}
                buttonStyle={styles.button}
                onPress={() => alert("favs")}
            >
            </Button>

        </View>

        {/* See on the map part */}
        <View style={styles.map}>
            <Text style={styles.heading}>See on the map</Text>
            
            {/* Return map page with selected bus route highlighted */}
            <Button                
                icon={<Icon iconStyle={styles.icon} name="arrow-right" type="font-awesome"/>}
                buttonStyle={styles.button}
                onPress={() => router.push('/map')}
            >
            </Button>
        </View>

        <TripInfo bus={sortedBus} />

    </SafeAreaView>
);
}

const styles = StyleSheet.create({
    first: {
        width: '20%'
    },
    second: {
        width: '60%',
        flexShrink: 0,
        paddingRight: 10
    },
    third: {
        width: '20%'
    },
    background: {
        paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
    },
    bus: {
        alignItems: 'center',
        flexDirection: 'row',
        height: '10%',
        width: '100%',
        backgroundColor: colors.backgroundPrimary,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    route: {
        backgroundColor: colors.backgroundSecondary,
        color: colors.textPrimary,
        fontSize: fonts.heading,
    },
    heading: {
        color: colors.textPrimary,
        flexGrow: 3,
        flexDirection: 'column',
        fontSize: fonts.heading,
    },
    button: {
        flexGrow: 1,
        color: colors.backgroundPrimary,
        backgroundColor: colors.backgroundPrimary,
    },
    icon: {
        color: colors.textPrimary,
    },
    map: {
        padding: 3,
        paddingHorizontal: 15,
        alignItems: 'center',
        flexDirection: 'row',
        width: '100%',
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    path: {
        height: '70%'
    },
    busPathVisited: {
        color: colors.objectSelected,
    },
    busPathNotVisited: {
        color: colors.objectNotSelected,
    },
    textPrimary: {
        padding: 7,
        textAlign: 'left',
        fontSize: fonts.heading,
        color: colors.textPrimary
    },
    textSecondary: {
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    time: {
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    textDescription: {
        color: colors.textSecondary,
        fontSize: fonts.body,
    },
    description: {
        justifyContent: 'space-evenly',
        flexDirection: 'row',
    },
    stop: {
        flexDirection: 'row', 
        paddingTop: 20,
        width: '100%',
    }
});