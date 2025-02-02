import React from 'react';
import { View, ScrollView, StyleSheet, TouchableOpacity, Text } from 'react-native';
import { Button } from 'react-native-elements';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';

const ButtonList = ({buttonData}) => {

    const handlePress = (title) => {
        alert(`You pressed ${title}`);
    };

    return (
        <ScrollView>
            {buttonData.map((item) => (
                <View key={item.id} style={styles.buttonContainer}>
                    <TouchableOpacity
                    style={styles.buttonContainer}
                    // {/* onPress={() => handlePress(item.title)} */}
                    onPress={() => router.push("/screens/stop")}
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
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    buttonContainer: {
        backgroundColor: colors.backgroundPrimary,
        padding: 5,
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

export default ButtonList;