import React from 'react';
import {StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';
import {Route} from "@/types/route";

const SearchButtonRoute = ({ item }: { item: Route }) => {
    return (
        <View style={styles.buttonContainer}>
            <TouchableOpacity
                style={styles.buttonContainer}
                // onPress={() => router.push({ pathname: `/screens/filtered_map/${item.name}`, params: { route: item.name } })}
                onPress={() => router.push(`/screens/filtered_map/${item.name}`)}
                activeOpacity={0.1}
            >
                <View style={styles.routeContainer}>
                    <Text style={styles.textPrimary}>
                        {`${item.name}`}  
                    </Text>
                </View>
            </TouchableOpacity>
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
        color: colors.textSwitchable,
        paddingVertical: 5,
        textAlign: 'center',
    },
    textSecondary: {
        fontSize: fonts.body,
        color: colors.textSecondary,
        
    },
    routeContainer: {
        backgroundColor: colors.backgroundSecondary,
        width: '15%',
        borderRadius: 10,
    }
});

export default SearchButtonRoute;