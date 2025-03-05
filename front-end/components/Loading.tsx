import React from 'react';
import {ActivityIndicator, StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';
import { SafeAreaView } from 'react-native-safe-area-context';

const Loading = ({ text }) => {
    return (
        <SafeAreaView style={styles.loading}>
                <Text>{text}</Text>
                <ActivityIndicator size="large" color="#00ff00" />
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    buttonContainer: {
        backgroundColor: colors.backgroundPrimary,
        padding: 5,
        paddingHorizontal: 7,
    },
    loading: {
        backgroundColor: colors.backgroundPrimary,
        textAlign: "center",
    },
    
});

export default Loading;