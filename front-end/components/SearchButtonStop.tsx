import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router, useLocalSearchParams} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';

const SearchButtonStop = ({ item }) => {

    return (
        <View>
                <View key={item.id} style={styles.buttonContainer}>

                    <TouchableOpacity
                    style={styles.buttonContainer}
                    onPress={() => router.push({ pathname: `/screens/arrivals/${String(item.id)}`, params: { stop: item.id } })} // forward data of the selected bus to bus page
                    activeOpacity={0.1}
                    >
                        <View>
                            <Text style={styles.textPrimary}>
                                {`Stop ${item.code}`}       
                            </Text>
                            <Text style={styles.textSecondary}>
                                {`${item.name}`} 
                            </Text>
                        </View>

                    </TouchableOpacity>

                </View>
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

export default SearchButtonStop;