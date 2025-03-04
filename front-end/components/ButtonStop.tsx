import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';
import {Stop} from "@/types/stop";
import {useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";

const ButtonStop = () => {


    const stops = useSelector((state: RootState) => state.stop.stops);
    //Dummy data
    // const stop = [
    //     { id: 1, route: '220', headsign: 'University College, Cork', arrival: '14:52' },
    //     { id: 1, route: '220X', headsign: 'MTU', arrival: '14:42' },
    //     { id: 1, route: '212', headsign: 'Patrick', arrival: '15:32' }
    // ];

    return (
        <View>

            {/* create component for each stop */}
            {stops.map((stop: Stop) => (

                <View key={stop.id} style={styles.buttonContainer}>

                    <TouchableOpacity
                    style={styles.buttonContainer}
                    onPress={() => router.push({ pathname: `/screens/arrivals/${String(stop.id)}`, params: { stop: stop.id } })}      // forward data of the selected stop to stop page
                    activeOpacity={0.1}
                    >
                        <View>
                            <Text style={styles.textPrimary}>
                                {`Stop ${stop.code}`}  
                            </Text>
                            <Text style={styles.textSecondary}>
                                {`${stop.name}`}  
                            </Text>
                        </View>
                    </TouchableOpacity>

                </View>
            ))}
        </View>
    );
};

const styles = StyleSheet.create({
    buttonContainer: {
        backgroundColor: colors.backgroundPrimary,
        padding: 5,
        paddingHorizontal: 7,
    },
    textPrimary: {
        fontSize: fonts.subHeading,
        color: colors.textPrimary,
    },
    textSecondary: {
        fontSize: fonts.body,
        color: colors.textSecondary,
    },
});

export default ButtonStop;