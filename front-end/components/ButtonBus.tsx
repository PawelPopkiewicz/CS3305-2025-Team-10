import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';
import {Bus} from "@/types/bus";
import {shallowEqual, useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";

const ButtonBus = () => {


    const buses = useSelector((state: RootState) => state.bus.buses, shallowEqual);

    return (
        <View>

            {/* create component for each bus route */}
            {buses.map((bus: Bus) => (

                <View key={bus.id} style={styles.buttonContainer}>

                    <TouchableOpacity
                    style={styles.buttonContainer}
                    onPress={() => router.push({ pathname: `/screens/trip/${bus.id}`, params: { bus: bus.id } })} // forward data of the selected bus to bus page
                    activeOpacity={0.1}
                    >
                        <View>
                            <Text style={styles.textPrimary}>
                                {`Bus ${bus.route}`}       
                            </Text>
                            <Text style={styles.textSecondary}>
                                {`${bus.headsign}`}
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

export default ButtonBus;