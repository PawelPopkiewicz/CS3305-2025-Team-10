import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';
import {useBusData} from "@/hooks/useBusData";
import {Bus} from "@/types/bus";

const ButtonBus = () => {

    const { buses } = useBusData();

    // dummy data
    // const bus = [
    //     { id: 1, code: '2232', name: 'University College, Cork', arrival: '14:32' },
    //     { id: 2, code: '7890', name: 'City Centre, Cork', arrival: '15:45' },
    //     { id: 3, code: '4567', name: 'Kent Station, Cork', arrival: '15:00' }
    // ]

    return (
        <View>

            {/* create component for each bus route */}
            {buses.map((bus: Bus) => (

                <View key={bus.id} style={styles.buttonContainer}>

                    <TouchableOpacity
                    style={styles.buttonContainer}
                    onPress={() => router.push({ pathname: `/screens/trip/${String(bus.id)}`, params: { bus: bus.id } })} // forward data of the selected bus to bus page
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