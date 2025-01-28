import {StyleSheet, View} from "react-native";
import ButtonTab from "../../components/ButtonTab";
import TransitFilter from "../../components/TransitFilter";
import MapView from 'react-native-maps';


export default function MobileMap() {

    return (
        <View style={styles.container}>
        <TransitFilter/>
            <MapView/>
            <ButtonTab />
        </View>
    )
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
    }
})