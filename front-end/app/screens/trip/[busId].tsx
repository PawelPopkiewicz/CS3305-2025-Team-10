import {Platform, SafeAreaView, ScrollView, StatusBar, StyleSheet, Text, View} from "react-native";
import {Button, Icon} from 'react-native-elements';
import {router, useFocusEffect, useLocalSearchParams} from 'expo-router';
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {useCallback, useState} from "react";
import {busApiUrl} from "@/config/constants";
import {shallowEqual, useDispatch, useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";
import {addFavoriteRoute, removeFavoriteRoute} from "@/app/redux/favRoutesSlice";
import Loading from "@/components/Loading";
import ErrorData from "@/components/ErrorData";

type StopInfo = { stopId: string, code: string, name: string, arrival: string };

const TripDisplay = ({ trip }: { trip: StopInfo[] }) => (
    <ScrollView style={styles.path}>
        {trip.map((stop) => (
            <View key={stop.stopId} style={styles.stop}>
                <View style={styles.firstRow}>
                    <Icon iconStyle={styles.busPathVisited} name="arrow-down" type="font-awesome" />
                </View>
                <View style={styles.secondRow}>
                    <Text style={styles.textSecondary}>
                        {`Stop ${stop.code} ${stop.name}`}
                    </Text>
                </View>
                <View style={styles.thirdRow}>
                    <Text style={styles.time}>{stop.arrival}</Text>
                </View>
            </View>
        ))}
    </ScrollView>
);

export default function TripScreen() {
    const { busId } = useLocalSearchParams() as { busId: string };
    const [trip, setTrip] = useState<StopInfo[]>([]);
    const buses = useSelector((state: RootState) => state.bus.buses, shallowEqual);
    const favRoutes = useSelector((state: RootState) => state.favRoute.routes, shallowEqual);
    const busData = buses.find(bus => bus.id === busId);
    const dispatch = useDispatch();


    useFocusEffect(
        useCallback(() => {
            const fetchTrip = async () => {
                try {
                    const response = await fetch(`${busApiUrl}/v1/trips/${busId}`, {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    const data: StopInfo[] = await response.json();
                    setTrip(data);
                } catch (error) {
                    console.error("Error fetching trips data:", error);
                }
            };

            fetchTrip();
            const interval = setInterval(fetchTrip, 10000);
            return () => clearInterval(interval);
        }, [busId])
    );

    if (!busData) return <ErrorData text="This bus isn't tracked anymore" />;
    const isFav = favRoutes?.includes(busData.route) ?? false;
    if (trip.length === 0) return <Loading text="Fetching bus data" />;


    // @ts-ignore
    // @ts-ignore
    return (
        <SafeAreaView style={styles.background}>
            <View style={styles.bus}>

                <View style={styles.firstRowBus}>

                    <Button
                        icon={<Icon iconStyle={styles.icon} name="chevron-left" type="font-awesome" />}
                        buttonStyle={styles.button}
                        onPress={() => router.back()}
                    />
                </View>

                {/* Wrap busData.route and busData.headsign in <Text> */}
                <View style={styles.secondRowBus}>
                    <Text style={styles.textRoute}>{busData.route}</Text>
                </View>

                <View style={styles.thirdRowBus}>
                    <Text style={styles.textPrimary}>{busData.headsign}</Text>
                </View>
                <View style={styles.fourthRowBus}>

                    <Button
                        icon={<Icon iconStyle={styles.icon} name={isFav ? "star" : "star-o"}
                                    type="font-awesome"/>}
                        buttonStyle={styles.button}
                        onPress={() => {
                            isFav ? dispatch(removeFavoriteRoute(busData.route)) : dispatch(addFavoriteRoute(busData.route))
                        }}
                    />
                </View>
            </View>

            <View style={styles.map}>
                <View style={styles.firstRowMap}>
                    <Text style={styles.heading}>See on the map</Text>
                </View>

                <View style={styles.secondRowMap}>
                    <Button
                        icon={<Icon iconStyle={styles.icon} name="arrow-right" type="font-awesome" />}
                        buttonStyle={styles.button}
                        onPress={() => router.push(`/screens/filtered_map/${busData.route}`)}
                    />
                </View>
            </View>

            <TripDisplay trip={trip} />
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    firstRow: {
        width: '20%'
    },
    secondRow: {
        width: '60%', 
        flexShrink: 0, 
        paddingRight: 10
    },
    thirdRow: {
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
    firstRowBus: {
        width: '15%'
    },
    secondRowBus: {
        backgroundColor: colors.backgroundSecondary,
        width: '20%',
        borderRadius: 10
    },
    thirdRowBus: {
        width: '50%',
        flexShrink: 0
    },
    fourthRowBus: {
        width: '15%'
    },
    heading: {
        color: colors.textPrimary,
        fontSize: fonts.heading
    },
    button: {
        backgroundColor: colors.backgroundPrimary
    },
    icon: {
        color: colors.textPrimary
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
    firstRowMap: {
        width: '85%',
    },
    secondRowMap: {
        width: '15%',
    },
    path: {
        height: '70%'
    },
    busPathVisited: {
        color: colors.objectSelected
    },
    textPrimary: {
        padding: 7,
        textAlign: 'left',
        fontSize: fonts.heading,
        color: colors.textPrimary,
    },
    textRoute: {
        padding: 7,
        textAlign: 'center',
        fontSize: fonts.heading,
        color: colors.textSwitchable,
        fontWeight: 'bold',
    },
    textSecondary: {
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    time: {
        color: colors.textPrimary,
        fontSize: fonts.subHeading
    },
    stop: {
        flexDirection: 'row',
        paddingTop: 20, width: '100%'
    },
});

