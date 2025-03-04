import {Marker} from "react-native-maps";
import {View, Text, Image} from "react-native";
import {router} from "expo-router";
import {Bus} from "@/types/bus";
import {useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";

const BusMarker = () => {

    const buses = useSelector((state: RootState) => state.bus.buses);
    const customBus = Image.resolveAssetSource(require('@/assets/images/bus.png')).uri

    return (
        buses.map((bus: Bus) => (
                <Marker
                    key={bus.id}
                    coordinate={{ latitude: bus.lat, longitude: bus.lon }}
                    pinColor="blue"
                    title="Bus"
                    description="Live Bus Location"
                    onPress={() => router.push({ pathname: `/screens/trip/${String(bus.id)}`, params: { bus: bus.id } })}
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
        ))
    );
};

export default BusMarker;