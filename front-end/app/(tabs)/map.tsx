import React, {useState} from "react";
import {View, Text, StyleSheet, TouchableOpacity, Image, SafeAreaView, Platform} from "react-native";
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
    const customBus = Image.resolveAssetSource(require('@/assets/images/Bus.png')).uri
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

    const CustomMarkerBus = ({busNumber}) => (
        <View style={{ alignItems: 'center' }}>
            {/* Bus Number Label */}
            <Text style={{ backgroundColor: 'black', padding: 4, borderRadius: 5, fontWeight: 'bold', color:'white' }}>
            {busNumber}
            </Text>

            <View style={{ transform: [{ rotate: '45deg' }] }}> 
            <Image
                source={{uri:customBus}}
                style={{ width: 25, height: 25, resizeMode: 'contain' }}
            />
            </View>
        </View>
      );
    
    const CustomMarkerStop = ({ }) => (
        <View style={{ transform: [{ rotate: '0deg' }] }}> 
            <Image
                source={{uri:customBusStop}}
                style={{ width: 25, height: 25, resizeMode: 'contain' }}
            />
            </View>
    )
    

    return (
        
        <SafeAreaView style={styles.background}>

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
                    />
                ): null

                ))}

                Bus Markers

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
                ))} */}

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
            // paddingTop: Platform.OS === 'android' ? 20 : 0,
            // paddingTop: 20,
            flex: 1,
            // justifyContent: 'flex-end',
            backgroundColor: colors.backgroundPrimary,
            // height: '100%'
            overflow: 'hidden',
            // borderRadius: 30,
        },
    input: {
        // backgroundColor: 'white',
        // paddingTop: 100,
        // top:70,
        marginTop: Platform.OS === 'android' ? 20 : 0,
        // marginBottom: 10,
        overflow: 'hidden',
        // alignItems: "center",
        borderRadius: 30,
        borderWidth: 1,
        // borderTopLeftRadius: 30,
        // borderTopRightRadius: 30,
        // borderTopWidth: 1,
        // borderLeftWidth: 1,
        // borderRightWidth: 1,
        // padding: 3,
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
