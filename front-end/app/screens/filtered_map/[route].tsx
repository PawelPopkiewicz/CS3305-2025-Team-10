import React, {useCallback, useState} from "react";
import {Platform, SafeAreaView, StatusBar, StyleSheet, Text, TouchableOpacity} from "react-native";
import {Icon} from '@rneui/themed';
import MapView, {Region} from "react-native-maps";
import {router, useLocalSearchParams} from "expo-router";
import {shallowEqual, useSelector} from "react-redux";
import BusMarker from "@/components/BusMarker";
import StopMarker from "@/components/StopMarker";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {RootState} from "@/app/redux/store";
import {DEFAULT_REGION} from "@/config/constants";
import ErrorData from "@/components/ErrorData";

const FilteredMap = () => {
    const { param_route } = useLocalSearchParams() as { param_route: string };
    const stops = useSelector((state: RootState) => state.stop.stops, shallowEqual);
    const buses = useSelector((state: RootState) => state.bus.buses, shallowEqual);
    const routes = useSelector((state: RootState) => state.route.routes, shallowEqual);
    const [region, setRegion] = useState<Region>(DEFAULT_REGION);

    const routeData = routes.find(route => route.name === param_route)
    if (!routeData) {
        return <ErrorData text={"Route not found"} />
    }
    // Filter only visible markers
    const getVisibleMarkers = useCallback(() => {
        return {
            visibleStops: stops.filter(stop =>
                routeData.stop_ids.includes(stop.id) &&
                stop.lat > region.latitude - region.latitudeDelta / 2 &&
                stop.lat < region.latitude + region.latitudeDelta / 2 &&
                stop.lon > region.longitude - region.longitudeDelta / 2 &&
                stop.lon < region.longitude + region.longitudeDelta / 2
            ),
            visibleBuses: buses.filter(bus =>
                bus.lat > region.latitude - region.latitudeDelta / 2 &&
                bus.lat < region.latitude + region.latitudeDelta / 2 &&
                bus.lon > region.longitude - region.longitudeDelta / 2 &&
                bus.lon < region.longitude + region.longitudeDelta / 2 &&
                bus.route === param_route
            )
        };
    }, [stops, buses, region]);

    const { visibleStops, visibleBuses } = getVisibleMarkers();

    return (
        <SafeAreaView style={styles.background}>
            <TouchableOpacity style={styles.input} onPress={() => router.push("/screens/search")}>
                <Icon iconStyle={styles.back} onPress={() => router.back()} name="chevron-left" type="font-awesome" />
                <Text style={styles.textSecondary}>Search bus stop or route</Text>
            </TouchableOpacity>

            <MapView
                style={{ flex: 1 }}
                initialRegion={region}
                rotateEnabled={false}
                onRegionChangeComplete={setRegion} // Updates visible markers
                // clusteringEnabled
                // clusterColor={colors.objectSelected}
                // clusterTextColor="#fff"
            >
                {/* Display Stop Markers */}
                {visibleStops.map((stop) => (
                    <StopMarker
                        key={stop.id}
                        id={stop.id}
                        lat={stop.lat}
                        lon={stop.lon}
                        name={stop.name}
                        code={stop.code}
                    />
                ))}

                {/* Bus Markers */}
                {visibleBuses.map((bus) => (
                    <BusMarker key={bus.id} lat={bus.lat} lon={bus.lon} id={bus.id} route={bus.route} direction={bus.direction} />
                ))}
            </MapView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    background: {
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
        overflow: 'hidden',
    },
    input: {
        marginTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
        overflow: 'hidden',
        borderRadius: 30,
        borderWidth: 1,
        flexDirection: 'row',
        paddingVertical: 15,
        paddingHorizontal: 20,
        borderColor: colors.border,
    },
    back: {
        color: colors.textPrimary,
        paddingRight: 20,
    },
    textSecondary: {
        color: colors.textSecondary,
        fontSize: fonts.subHeading,
    }
});

export default FilteredMap;
