import {Marker} from "react-native-maps";
import {View, Image} from "react-native";
import {router} from "expo-router";

import {useBusData} from "@/hooks/useBusData";
import {Stop} from "@/types/stop";

const StopMarker = () => {

    const { stops } = useBusData();
    const customBusStop = Image.resolveAssetSource(require('@/assets/images/BusStop.png')).uri

    return (
        stops.map((stop: Stop) => (
            <Marker
            key={stop.id}
            coordinate={{ latitude: stop.lat, longitude: stop.lon }}
            title={stop.name}
            description="Bus Stop"
            onPress={() => router.push({ pathname: `/screens/arrivals/${String(stop.id)}`, params: { stop: stop.id } })}
            >
                <View> 
                    <Image
                        source={{uri:customBusStop}}
                        style={{ width: 25, height: 25, resizeMode: 'contain' }}
                    />
                </View>
            </Marker>
        ))
    );
};

export default StopMarker;