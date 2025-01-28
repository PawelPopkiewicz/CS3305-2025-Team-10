import { Platform } from 'react-native';
import MobileMap from '@/app/screens/mobileMap';
import WebMap from '@/app/screens/webMap';

export default function Map() {
    return Platform.OS === 'web' ? <WebMap /> : <MobileMap />;
}