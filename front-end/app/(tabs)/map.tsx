import React, {useState} from "react";
import {View, Text, StyleSheet, TouchableOpacity} from "react-native";
import {Icon, Input} from '@rneui/themed';
import MapView, {Marker} from "react-native-maps";
import {useBusData} from "@/hooks/useBusData";
import {router} from "expo-router";

import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {Stop} from "@/types/stop";
import {Bus} from "@/types/bus";

const Map = () => {
    const { stops, buses } = useBusData();
    const [text, setText] = useState("");
    return (
        
        <View style={styles.background}>

            {/* <Input
            inputStyle={styles.textPrimary}
            inputContainerStyle={styles.input}
            value={text} // Controlled input
            onChangeText={setText} // Update state on change
            placeholder="Search bus stop or route"
            rightIcon={<Icon iconStyle={styles.clear} onPress={() => setText("")} name="plus" type="font-awesome"/>}
            leftIcon={<Icon iconStyle={styles.back} onPress={() => router.back()} name="chevron-left"
                            type="font-awesome"/>}
            >
            </Input> */}
            <TouchableOpacity style={styles.input} onPress={() => router.push("/screens/search")}><Text style={styles.textSecondary}>Search bus stop or route</Text></TouchableOpacity>
            <MapView
                style={{ flex: 1 }}
                initialRegion={{
                    latitude: 51.8940,
                    longitude: -8.4900,
                    latitudeDelta: 0.03,
                    longitudeDelta: 0.03,
                }}
            >
                {/* Bus Stop Markers */}
                {stops?.length > 0 && stops.map((stop: Stop) => (
                    stop.lat && stop.lon ? (
                        <Marker
                        key={stop.id}
                        coordinate={{ latitude: stop.lat, longitude: stop.lon }}
                        title={stop.name}
                        description="Bus Stop"
                    />
                ): null

                ))}

                {/* Bus Markers */}

                {buses?.length > 0 && buses.map((bus: Bus) => (
                    bus.lat && bus.lon ? (
                        <Marker
                            key={bus.id}
                            coordinate={{ latitude: bus.lat, longitude: bus.lon }}
                            pinColor="blue"
                            title="Bus"
                            description="Live Bus Location"
                        />
                    ) : null
                ))}

                {/* Example Route Line

                <Polyline
                    coordinates={busRoutes.map((stop: { latitude: number; longitude: number; }) => ({
                        latitude: stop.latitude,
                        longitude: stop.longitude,
                    }))}
                    strokeWidth={3}
                    strokeColor="red"
                />
                */}

            </MapView>
            
        </View>
    );
};

const styles = StyleSheet.create({
    background: {
            // paddingTop: Platform.OS === 'android' ? 20 : 0,
            // paddingTop: 20,
            flex: 1,
            // justifyContent: 'flex-end',
            backgroundColor: colors.backgroundPrimary,
            // height: '100%'
        },
    input: {
        // paddingTop: 100,
        // top:70,
        marginTop:70,
        // alignItems: "center",
        borderRadius: 30 ,
        borderWidth: 2,
        // padding: 3,
        paddingVertical: 15,
        paddingHorizontal: 15,
        borderColor: colors.border,
    },
    clear: {
        color: colors.textPrimary,
        transform: [{rotate: "45deg"}],
    },
    back: {
        color: colors.textPrimary
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
