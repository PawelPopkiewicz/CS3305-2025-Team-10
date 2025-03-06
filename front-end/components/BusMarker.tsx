import React, { useMemo } from "react";
import { Marker } from "react-native-maps";
import { View, Text, Image, StyleSheet } from "react-native";
import { router } from "expo-router";

interface BusProps {
    id: string;
    lat: number;
    lon: number;
    route: string;
    direction: number;
}

const BusMarker: React.FC<BusProps> = ({ id, lat, lon, route, direction }) => {
    // Cache bus icon
    const customBus = useMemo(() => Image.resolveAssetSource(require('@/assets/images/bus.png')).uri, []);

    return (
        <Marker
            key={id}
            coordinate={{ latitude: lat, longitude: lon }}
            title={`Bus ${route}`}
            description="Live Bus Location"
            onPress={() => router.push(`/screens/trip/${id}`)}
        >
            <View style={{ alignItems: 'center' }}>
                {/* Bus route label */}
                <Text style={styles.routeText}>{route}</Text>

                {/* Rotated bus image */}
                <View style={{ transform: [{ rotate: `${direction}deg` }] }}> 
                    <Image
                        source={{ uri: customBus }}
                        style={styles.busIcon}
                    />
                </View>
            </View>
        </Marker>
    );
};

// Optimize re-renders
export default React.memo(BusMarker);

const styles = StyleSheet.create({
    routeText: {
        backgroundColor: 'black',
        padding: 4,
        borderRadius: 5,
        fontWeight: 'bold',
        color: 'white',
    },
    busIcon: {
        width: 25,
        height: 25,
        resizeMode: 'contain',
    },
});
