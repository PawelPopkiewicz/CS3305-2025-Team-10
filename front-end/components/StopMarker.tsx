import {Marker} from "react-native-maps";
import {Image, View} from "react-native";
import {router} from "expo-router";
import {Stop} from "@/types/stop";
import {useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";

const StopMarker = () => {


    const stops = useSelector((state: RootState) => state.stop.stops);
    const customBusStop = Image.resolveAssetSource(require('@/assets/images/BusStop.png')).uri

    return (
        stops.map((stop: Stop) => (
            <Marker
            key={stop.id}
            coordinate={{ latitude: stop.lat, longitude: stop.lon }}
            title={stop.name}
            description="Bus Stop"
            onPress={() => router.push({ pathname: `/screens/arrivals/${stop.id}`, params: { stop: stop.id } })}
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