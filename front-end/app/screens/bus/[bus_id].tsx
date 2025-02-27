import {Platform, SafeAreaView, ScrollView, StyleSheet, Text, View, StatusBar} from "react-native";
import {Button, Icon} from 'react-native-elements';
import {router, useFocusEffect, useLocalSearchParams} from 'expo-router';
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {useCallback, useEffect, useState} from "react";
import {busApiUrl} from "@/config/constants";
import {useBusData} from "@/hooks/useBusData";

type StopInfo = {'stopId': number, 'code': string, 'name': string, 'arrival': string}

const TripDisplay = ({ trip }: { trip: StopInfo[] }) => (

    // Display each stop of the selected bus ordered by arrival time
    <ScrollView style={styles.path}>

        {/* component for each stop */}
        {trip.map((stop) => (

            <View key={stop.stopId} style={styles.stop}>
                <View style={styles.first}>
                    <Icon iconStyle={styles.busPathVisited} name="arrow-down" type="font-awesome"/>
                </View>
                <View style={styles.second}>
                    <Text style={styles.textSecondary}>{`Stop ${stop.code} ${stop.name}`}</Text>      {/* Stop info i.e. Stop 223 University College Cork */}
                </View>
                <View style={styles.third}>
                    <Text style={styles.time}>{stop.arrival}</Text>      {/* arrival time */}
                </View>
            </View>
        ))}
    </ScrollView>
);

export default function Bus_id() {
    const {bus_id} = useLocalSearchParams() as { bus_id: string };
    const [trip, setTrip] = useState<StopInfo[]>([]);
    const {buses} = useBusData();

    useFocusEffect(
        useCallback(() => {
        const fetchTrips = async () => {
            try {
                const response = await fetch(`${busApiUrl}/v1/trips/${parseInt(bus_id)}`, {
                    method: "GET",
                    headers: {"Content-Type": "application/json"},
                });
                console.log(`${busApiUrl}/v1/trips/${parseInt(bus_id)}`);
                console.log(response);
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data : StopInfo[] = await response.json();
                setTrip(data);
            } catch (error) {
                console.error("Error fetching trips data:", error);
            }
        };

        // Fetch initially and then set up interval
        fetchTrips();
        const interval = setInterval(fetchTrips, 10000);

        return () => clearInterval(interval); // Cleanup interval on unmount
    }, [bus_id])
    );

    // We can make a loading screen later
    if (trip.length === 0) return <Text>Loading...</Text>;
    const busData = buses.find(bus => bus.id === +bus_id); //converting to number
    if (!busData) return <Text>This bus isn't tracked anymore</Text>;

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
                <Text style={styles.textPrimary}>{busData.route}</Text>
            </View>

            <View style={styles.heading}>
                <Text style={styles.textPrimary}>{busData.headsign}</Text>
            </View>

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

        <TripDisplay trip={trip} />

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