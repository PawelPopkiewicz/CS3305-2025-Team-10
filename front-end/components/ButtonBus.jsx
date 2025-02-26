import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';

const ButtonBus = ({buttonData}) => {

    const bus = [
        { id: 1, code: '2232', name: 'University College, Cork', arrival: '14:32' },
        { id: 2, code: '7890', name: 'City Centre, Cork', arrival: '15:45' },
        { id: 3, code: '4567', name: 'Kent Station, Cork', arrival: '15:00' }
    ]
    const handlePress = (title) => {
        alert(`You pressed ${title}`);
    };

    return (
        <View>
            {buttonData.map((item) => (
                <View key={item.id} style={styles.buttonContainer}>
                    <TouchableOpacity
                    style={styles.buttonContainer}
                    // {/* onPress={() => handlePress(item.title)} */}
                    onPress={() => router.push({ pathname: '/screens/bus', params: { bus: JSON.stringify(bus) } })}
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
        // borderBottomWidth: 1,
        // borderBottomColor: colors.border,
        // justifyContent: 'left',
    },
    // button: {
    //     backgroundColor: colors.backgroundPrimary,
    //     justifyContent: 'flex-start',
    // },
    // title: {
    //     textAlign: 'left',
    //     // padding: 7,
    //     fontSize: fonts.subHeading,
    // },
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