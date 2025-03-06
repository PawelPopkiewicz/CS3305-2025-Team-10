import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';
import {Stop} from "@/types/stop";
import {shallowEqual, useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";

const ButtonStop = () => {
    const stops = useSelector((state: RootState) => state.stop.stops, shallowEqual);
    const favs = useSelector((state: RootState) => state.favStop.stops ?? [], shallowEqual);
    const favStops = stops.filter((stop: Stop) => favs?.includes?.(stop.id));

    return (
        <View>

            {/* create component for each stop */}
            {favStops.map((stop: Stop) => (

                <View key={stop.id} style={styles.buttonContainer}>

                    <TouchableOpacity
                    style={styles.buttonContainer}
                    onPress={() => router.push({ pathname: `/screens/arrivals/${stop.id}`, params: { stop: stop.id } })}      // forward data of the selected stop to stop page
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