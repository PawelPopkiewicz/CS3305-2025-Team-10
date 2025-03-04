import React, { useMemo } from "react";
import { Marker } from "react-native-maps";
import { Image, View } from "react-native";
import { router } from "expo-router";

interface StopProps {
    id: string;
    lat: number;
    lon: number;
    name: string;
    code: string;
}

const StopMarker: React.FC<StopProps> = ({ id, lat, lon, name, code }) => {
    // Cache bus stop icon
    const customBusStop = useMemo(
        () => Image.resolveAssetSource(require('@/assets/images/BusStop.png')).uri,
        []
    );

    return (
        <Marker
            key={id}
            coordinate={{ latitude: lat, longitude: lon }}
            title={name}
            description="Bus Stop"
            onPress={() => router.push({ pathname: `/screens/arrivals/${id}`, params: { stop: id } })}
        >
            <View>
                <Image source={{ uri: customBusStop }} style={styles.stopIcon} />
            </View>
        </Marker>
    );
};

// Optimize re-renders
export default React.memo(StopMarker);

const styles = {
    stopIcon: {
        width: 15,
        height: 15,
        resizeMode: "contain",
    },
};
