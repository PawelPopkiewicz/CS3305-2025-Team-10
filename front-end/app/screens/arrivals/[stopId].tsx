import {Platform, SafeAreaView, ScrollView, StatusBar, StyleSheet, Text, View} from "react-native";
import {Button, Icon} from 'react-native-elements';
import {router, useFocusEffect, useLocalSearchParams} from 'expo-router';
import {useDispatch, useSelector} from "react-redux";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {RootState} from "@/app/redux/store";
import {addFavoriteStop, removeFavoriteStop} from "@/app/redux/favSlice";
import {useCallback, useState} from "react";
import {busApiUrl} from "@/config/constants";

type BusInfo = { 'busId': string, 'route': string, 'headsign': string, 'arrival': string }

const ArrivalsDisplay = ({arrivals}: { arrivals: BusInfo[] }) => (

    // Display each arriving bus of selected bus stop ordered by arrival time

    <ScrollView>
        {arrivals.map((bus: BusInfo) => (
            //create component for each bus
            <View key={bus.busId} style={styles.bus}>
                <View style={styles.first}>
                    <Text style={styles.textSecondary}>{bus.route}</Text> {/* Bus route */}
                </View>
                <View style={styles.second}>
                    <Text style={styles.textSecondary}>{bus.headsign}</Text> {/* Headsign */}
                </View>
                <View style={styles.third}>
                    <Text style={styles.textSecondary}>{bus.arrival}</Text> {/* arrival time */}
                </View>
            </View>
        ))}
    </ScrollView>
);

export default function Stop() {

    const {stopId} = useLocalSearchParams() as { stopId: string };
    const [arrivals, setArrivals] = useState<BusInfo[]>([]);
    const stops = useSelector((state: RootState) => state.stop.stops);
    useFocusEffect(
        useCallback(() => {
            const fetchTrip = async () => {
                try {
                    const response = await fetch(`${busApiUrl}/v1/arrivals/${stopId}`, {
                        method: "GET",
                        headers: {"Content-Type": "application/json"},
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }

                    const data: BusInfo[] = await response.json();
                    setArrivals(data);
                } catch (error) {
                    console.error("Error fetching trips data:", error);
                }
            };

            fetchTrip();
            const interval = setInterval(fetchTrip, 10000);

            return () => clearInterval(interval); // Cleanup interval on unmount
        }, [stopId])
    );
    const favStops = useSelector((state: RootState) => state.fav.favStops);
    const isFav = favStops.includes(stopId);
    const dispatch = useDispatch();
    const stopData = stops.find(stop => stop.id === stopId); //converting to number

    if (arrivals.length === 0) return (
        <SafeAreaView style={styles.background}>
            <Text style={styles.textPrimary}>Loading...</Text>
        </SafeAreaView>
    );

    if (!stopData) return (
        <SafeAreaView style={styles.background}>
            <Text style={styles.textPrimary}>This stop isn't tracked anymore</Text>
        </SafeAreaView>
    );

    return (

        <SafeAreaView
            style={styles.background}
        >
            {/* Chosen bus stop */}
            <View style={styles.stop}>

                <Button
                    icon={<Icon iconStyle={styles.icon} name="chevron-left" type="font-awesome"/>}      //go back button
                    buttonStyle={styles.button}
                    onPress={() => router.back()}
                />

                <View style={styles.heading}>
                    <Text style={styles.textPrimary}> {stopData?.name || 'Stop'} </Text>
                </View>

                <Button
                    icon={<Icon iconStyle={styles.icon} name= {isFav ? "star" : "star-o"} type="font-awesome"/>}        // favourite button
                    buttonStyle={styles.button}
                    onPress={() => {
                        isFav ? dispatch(removeFavoriteStop(stopId)) : dispatch(addFavoriteStop(stopId))
                    }}
                />
            </View>

            {/* Description of displayed info component */}
            <View style={styles.description}>
                    <View style={styles.first}>
                        <Text style={styles.textDescription}>Route</Text>
                    </View>
                    <View style={styles.second}>
                        <Text style={styles.textDescription}>Direction</Text>
                    </View>
                    <View style={styles.third}>
                        <Text style={styles.textDescription}>Departs</Text>
                    </View>

            </View>

            <ArrivalsDisplay arrivals={arrivals}/>

        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    first: {
        width: '20%',
        alignItems: 'center'
    },
    second: {
        width: '60%',
        flexShrink: 0,
        alignItems: 'center'
    },
    third: {
        width: '20%',
        alignItems: 'center',
        paddingRight: 10,
    },
    background: {
        paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
    },
    stop: {
        alignItems: "center",
        flexDirection: 'row',
        height: '10%',
        backgroundColor: colors.backgroundPrimary,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    heading: {
        color: colors.textPrimary,
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
    textPrimary: {
        textAlign: 'left',
        fontSize: fonts.heading,
        color: colors.textPrimary
    },
    textSecondary: {
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    textDescription: {
        color: colors.textSecondary,
        fontSize: fonts.body,
    },
    description: {
        paddingTop: 20,
        justifyContent: 'space-evenly',
        flexDirection: 'row',
    },
    bus: {
        paddingTop: 20,
        flexDirection: 'row',
        width: '100%',
    }
});