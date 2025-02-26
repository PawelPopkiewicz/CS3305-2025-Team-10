import {Platform, SafeAreaView, ScrollView, StyleSheet, Text, View} from "react-native";
import {Button, Icon} from 'react-native-elements';
import {router, useLocalSearchParams} from 'expo-router';
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {useDispatch, useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";
import {addFavoriteStop, removeFavoriteStop} from "@/app/redux/favSlice";

const ArrivingBuses = ({ stop }) => (
    // Display each arriving bus of selected bus stop ordered by arrival time, barebones given below 

    <ScrollView style={styles.departures}>
        {stop.map((bus) => (
            <View key={bus.id} style={styles.bus}>
                <View style={styles.first}>
                    <Text style={styles.textSecondary}>{`${bus.route}`}</Text>
                </View>
                <View style={styles.second}>
                    <Text style={styles.textSecondary}>{`${bus.headsign}`}</Text>
                </View>
                <View style={styles.third}>
                    <Text style={styles.textSecondary}>{`${bus.arrival}`}</Text>
                </View>
            </View>
        ))}
    </ScrollView>
);

export default function Stop() {

    const params = useLocalSearchParams();
    const stop = params.stop ? JSON.parse(params.stop) : [];
    
    // const bus = [
    //     { id: 1, code: '2232', name: 'University College, Cork', arrival: '14:32' },
    //     { id: 2, code: '7890', name: 'City Centre, Cork', arrival: '15:45' },
    //     { id: 3, code: '4567', name: 'Kent Station, Cork', arrival: '15:00' }
    // ]
    
    const sortedStop = [...stop].sort((a, b) => {
        return a.arrival.localeCompare(b.arrival);
    });

    const stopFav = "WGB";
    const favStops = useSelector((state: RootState) => state.fav.favStops);
    const isFav = favStops.includes(stopFav);
    const dispatch = useDispatch();
return (
    <SafeAreaView
        style={styles.background}
    >
        {/* Chosen bus stop */}
        <View style={styles.stop}>
            <Button
                icon={<Icon iconStyle={styles.icon} name="chevron-left" type="font-awesome"/>}
                buttonStyle={styles.button}
                onPress={() => router.back()}
                >

            </Button>
            <View style={styles.heading}>
                <Text style={styles.textPrimary}>Stop 2232 University College, Cork</Text>
            </View>
            <Button                
                icon={<Icon iconStyle={styles.icon} name= {isFav ? "star" : "star-o"} type="font-awesome"/>}
                buttonStyle={styles.button}
                onPress={() => { isFav ? dispatch(removeFavoriteStop(stopFav)) : dispatch(addFavoriteStop(stopFav)) }}
            >

            </Button>

        </View>

        {/* Description part */}
        <View style={styles.description}>
                <View style={styles.first}>
                    <Text style={styles.textDescription}>Route</Text>
                </View>
                <View style={styles.second}>
                    <Text style={styles.textDescription}>Direction</Text>
                </View>
                <View style={styles.third}>
                    <Text style={styles.textDescription}>Departs</Text>
                </View>

        </View>

        <ArrivingBuses stop={sortedStop} />

    </SafeAreaView>
);
}

const styles = StyleSheet.create({
    first: {width: '20%',alignItems: 'center'},
    second: {width: '60%', flexShrink: 0,alignItems: 'center'},
    third: {width: '20%',alignItems: 'center', paddingRight: 10,},
    background: {
        paddingTop: Platform.OS === 'android' ? 20 : 0,
        // paddingTop: 20,
        flex: 1,
        // justifyContent: 'flex-end',
        backgroundColor: colors.backgroundPrimary,
        // height: '100%'
    },
    stop: {
        alignItems: "center",
        flexDirection: 'row',
        height: '10%',
        // width: '100%',
        backgroundColor: colors.backgroundPrimary,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
        // padding: 3,
        // paddingHorizontal: 15,
    },
    heading: {
        color: colors.textPrimary,
        // flexGrow: 1,
        flexDirection: 'column',
        fontSize: fonts.heading,
    },
    button: {
        flexGrow: 1,
        color: colors.backgroundPrimary,
        backgroundColor: colors.backgroundPrimary,
    },
    icon: {
        color: colors.textPrimary,
    },
    textPrimary: {
        // padding: 7,
        textAlign: 'left',
        fontSize: fonts.heading,
        color: colors.textPrimary
    },
    textSecondary: {
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    textDescription: {
        color: colors.textSecondary,
        fontSize: fonts.body,
    },
    description: {
        paddingTop: 20,
        justifyContent: 'space-evenly',
        flexDirection: 'row',
    },
    departures: {
        
        // paddingTop: 20,
    },
    bus: {
        paddingTop: 20,
        // justifyContent: 'space-evenly',
        
        flexDirection: 'row', 
        width: '100%',
    }
});