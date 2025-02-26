import React, {useState} from "react";
import {View, Text, StyleSheet, TouchableOpacity, Image, SafeAreaView, Platform, StatusBar} from "react-native";
import {Icon} from '@rneui/themed';
import MapView, {Marker} from "react-native-maps";
import {router} from "expo-router";

import {useBusData} from "@/hooks/useBusData";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {Stop} from "@/types/stop";
import {Bus} from "@/types/bus";


const Map = () => {
    const { stops, buses } = useBusData();
    const [text, setText] = useState("");
    const customBus = Image.resolveAssetSource(require('@/assets/images/bus.png')).uri
    const customBusStop = Image.resolveAssetSource(require('@/assets/images/BusStop.png')).uri

    // const CustomMarker = ({ busNumber }) => (
    //     <View style={{ transform: [{ rotate: `45deg` }], alignItems: 'center' }}>
    //       {/* Image with Overlapping Text */}
          
          
    //       <Image
    //         source={{uri:customBus}}
    //         style={{ width: 100, height: 55, resizeMode: 'contain' }}
    //       />
    //       <View style={{ position: 'absolute',alignItems: 'center' }}>
    //         <Text style={{ color: 'white', fontWeight: 'bold', fontSize: 16, backgroundColor: 'rgba(0,0,0,0.6)', padding: 4, borderRadius: 5 }}>
    //           {busNumber}
    //         </Text>
    //       </View>
    //     </View>
    //   );

    // const CustomMarkerBus = ({busNumber}) => (
    //     <View style={{ alignItems: 'center' }}>
    //         <Text style={{ backgroundColor: 'black', padding: 4, borderRadius: 5, fontWeight: 'bold', color:'white' }}>
    //         {busNumber}
    //         </Text>

    //         <View style={{ transform: [{ rotate: '45deg' }] }}> 
    //         <Image
    //             source={{uri:customBus}}
    //             style={{ width: 25, height: 25, resizeMode: 'contain' }}
    //         />
    //         </View>
    //     </View>
    //   );
    
    // const CustomMarkerStop = ({ }) => (
    //     <View style={{ transform: [{ rotate: '0deg' }] }}> 
    //         <Image
    //             source={{uri:customBusStop}}
    //             style={{ width: 25, height: 25, resizeMode: 'contain' }}
    //         />
    //     </View>
    // )
    

    return (
        
        <SafeAreaView style={styles.background}>

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
                rotateEnabled={false} // Prevents map rotation}
            >
                {/* Bus Stop Markers */}
                {stops?.length > 0 && stops.map((stop: Stop) => (
                    stop.lat && stop.lon ? (

                        <Marker
                        key={stop.id}
                        coordinate={{ latitude: stop.lat, longitude: stop.lon }}
                        title={stop.name}
                        description="Bus Stop"
                        >
                            <View> 
                                <Image
                                    source={{uri:customBusStop}}
                                    style={{ width: 25, height: 25, resizeMode: 'contain' }}
                                />
                            </View>
                        </Marker>
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
                            onPress={() => router.push({ pathname: '/screens/bus', params: { bus: bus.id } })}
                        >
                            <View style={{ alignItems: 'center' }}>
                                {/* Bus route label */}
                                <Text style={{ backgroundColor: 'black', padding: 4, borderRadius: 5, fontWeight: 'bold', color:'white' }}>
                                {bus.route}
                                </Text>

                                <View style={{ transform: [{ rotate: `${bus.direction}deg` }] }}> 
                                <Image
                                    source={{uri:customBus}}
                                    style={{ width: 25, height: 25, resizeMode: 'contain' }}
                                />
                                </View>
                            </View>
                        </Marker>

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
        paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
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
