import React from "react";
import {Platform, SafeAreaView, StatusBar, StyleSheet, Text, TouchableOpacity} from "react-native";
import {Icon} from '@rneui/themed';
import MapView from "react-native-maps";
import {router} from "expo-router";
import BusMarker from "@/components/BusMarker";
import StopMarker from "@/components/StopMarker";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {Stop} from "@/types/stop";
import {Bus} from "@/types/bus";
import {shallowEqual, useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";

const Map = () => {

    const stops = useSelector((state: RootState) => state.stop.stops, shallowEqual);
    const buses = useSelector((state: RootState) => state.bus.buses, shallowEqual);

    return (
        
        <SafeAreaView style={styles.background}>

            {/*  */}
            <TouchableOpacity style={styles.input} onPress={() => router.push("/screens/search")}>
                <Icon iconStyle={styles.back} onPress={() => router.back()} name="chevron-left" type="font-awesome"/>
                <Text style={styles.textSecondary}>Search bus stop or route</Text>
            </TouchableOpacity>

            <MapView
                style={{ flex: 1 }}
                initialRegion={{
                    latitude: 51.8940,
                    longitude: -8.4900,
                    latitudeDelta: 0.03,
                    longitudeDelta: 0.03,
                }}
                rotateEnabled={false} // Prevents map rotation
            >

                {/* Display Stop Markers */}
                {stops?.length > 0 && stops.map((stop: Stop) => (
                    stop.lat && stop.lon ? (
                        <StopMarker />
                ): null

                ))}

                {/* Display Bus Markers */}

                {buses?.length > 0 && buses.map((bus: Bus) => (
                    bus.lat && bus.lon ? (
                        <BusMarker />
                    ) : null
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
        paddingHorizontal: 15,
        borderColor: colors.border,

    },
    clear: {
        color: colors.textPrimary,
        transform: [{rotate: "45deg"}],
    },
    back: {
        color: colors.textPrimary,
        paddingRight: 10,
    },
    textSelected: {
            color: colors.objectSelected,
            fontSize: fonts.subHeading
    },
    textPrimary:{
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    textSecondary: {
        color: colors.textSecondary,
        fontSize: fonts.subHeading,
    }
});
export default Map;
