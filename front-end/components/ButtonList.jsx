import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';

const ButtonList = ({buttonData}) => {

    //Dummy data
    const stop = [
        { id: 1, route: '220', headsign: 'University College, Cork', arrival: '14:52' },
        { id: 1, route: '220X', headsign: 'MTU', arrival: '14:42' },
        { id: 1, route: '212', headsign: 'Patrick', arrival: '15:32' }
    ];

    return (
        <View>
            {buttonData.map((item) => (
                <View key={item.id} style={styles.buttonContainer}>
                    <TouchableOpacity
                    style={styles.buttonContainer}

                    // pass information about the chosen stop on click
                    onPress={() => router.push({ pathname: '/screens/stop', params: { stop: JSON.stringify(stop) } })}
                    activeOpacity={0.1}
                    >
                        <View>
                            <Text style={styles.textPrimary}>
                                {item.title.split(",")[0]?.trim() || ""}
                            </Text>
                            <Text style={styles.textSecondary}>
                            {item.title.split(",")[1]?.trim() || ""}
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

export default ButtonList;