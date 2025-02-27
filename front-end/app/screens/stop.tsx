import {Platform, SafeAreaView, ScrollView, StyleSheet, Text, View, StatusBar} from "react-native";
import {Button, Icon} from 'react-native-elements';
import {router, useLocalSearchParams} from 'expo-router';
import {useDispatch, useSelector} from "react-redux";

import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {RootState} from "@/app/redux/store";
import {addFavoriteStop, removeFavoriteStop} from "@/app/redux/favSlice";

const ArrivingBuses = ({ stop }) => (

    // Display each arriving bus of selected bus stop ordered by arrival time
    <ScrollView>

        {stop.map((bus) => (
            //create component for each bus

            <View key={bus.id} style={styles.bus}>
                <View style={styles.first}>
                    <Text style={styles.textSecondary}>{`${bus.route}`}</Text>      {/* Bus route */}
                </View>
                <View style={styles.second}>
                    <Text style={styles.textSecondary}>{`${bus.headsign}`}</Text>   {/* Headsign */}
                </View>
                <View style={styles.third}>
                    <Text style={styles.textSecondary}>{`${bus.arrival}`}</Text>    {/* arrival time */}
                </View>
            </View>

        ))}
    </ScrollView>
);

export default function Stop() {

    const params = useLocalSearchParams();
    const stop = params.stop ? JSON.parse(params.stop) : [];
    
    // Dummy data
    // const bus = [
    //     { id: 1, code: '2232', name: 'University College, Cork', arrival: '14:32' },
    //     { id: 2, code: '7890', name: 'City Centre, Cork', arrival: '15:45' },
    //     { id: 3, code: '4567', name: 'Kent Station, Cork', arrival: '15:00' }
    // ]
    
    // sort data based in arriving time
    const sortedStop = [...stop].sort((a, b) => {
        return a.arrival.localeCompare(b.arrival);
    });

    // handle favourites
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
                    icon={<Icon iconStyle={styles.icon} name="chevron-left" type="font-awesome"/>}      //go back button
                    buttonStyle={styles.button}
                    onPress={() => router.back()}
                    >
                </Button>

                <View style={styles.heading}>
                    <Text style={styles.textPrimary}>Stop 2232 University College, Cork</Text>      {/* Name of the bus stop */}
                </View>

                <Button                
                    icon={<Icon iconStyle={styles.icon} name= {isFav ? "star" : "star-o"} type="font-awesome"/>}        // favourite button
                    buttonStyle={styles.button}
                    onPress={() => { isFav ? dispatch(removeFavoriteStop(stopFav)) : dispatch(addFavoriteStop(stopFav)) }}
                >
                </Button>

            </View>

            {/* Description of displayed info component */}
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
    first: {
        width: '20%',
        alignItems: 'center'
    },
    second: {
        width: '60%',
        flexShrink: 0,
        alignItems: 'center'
    },
    third: {
        width: '20%',
        alignItems: 'center',
        paddingRight: 10,
    },
    background: {
        paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
    },
    stop: {
        alignItems: "center",
        flexDirection: 'row',
        height: '10%',
        backgroundColor: colors.backgroundPrimary,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    heading: {
        color: colors.textPrimary,
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
    bus: {
        paddingTop: 20,
        flexDirection: 'row', 
        width: '100%',
    }
});