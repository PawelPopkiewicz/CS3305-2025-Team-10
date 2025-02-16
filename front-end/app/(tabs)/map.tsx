import React from "react";
import {View} from "react-native";
import MapView, {Marker} from "react-native-maps";
import {useBusData} from "@/hooks/useBusData";


const Map = () => {
    const { stops, busRoutes, busPositions } = useBusData();

    return (
        <View style={{ flex: 1 }}>
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
                {stops?.length > 0 && stops.map((stop: { id: any; latitude: number; longitude: number; name: string | undefined; }) => (
                    stop.latitude && stop.longitude ? (
                        <Marker
                        key={stop.id}
                        coordinate={{ latitude: stop.latitude, longitude: stop.longitude }}
                        title={stop.name}
                        description="Bus Stop"
                    />
                ): null

                ))}

                {/* Bus Markers */}

                {busPositions?.length > 0 && busPositions.map((bus: { id: any; latitude: number; longitude: number }) => (
                    bus.latitude && bus.longitude ? (
                        <Marker
                            key={bus.id}
                            coordinate={{ latitude: bus.latitude, longitude: bus.longitude }}
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

export default Map;
