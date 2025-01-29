import {Platform} from 'react-native';


const MapComponent = Platform.OS === 'web'
    ? require('./webMap').default
    : require('./mobileMap').default;


export default function Map() {
    return (
        <MapComponent/>
    )
}