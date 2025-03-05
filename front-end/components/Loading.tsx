import React from 'react';
import {ActivityIndicator, StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';


const Loading = ({ text }: { text: String }) => {
    return (
        <SafeAreaView style={styles.loading}>
                <Text style={styles.textData}>{text}</Text>
                <ActivityIndicator size="large" color={colors.objectSelected} />
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    textData: {
        color: colors.textPrimary,
        textAlign: "center",
        fontSize: 24,
    },
    loading: {
        backgroundColor: colors.backgroundPrimary,
        textAlign: "center",
        justifyContent: 'center',
        alignContent: 'center',
        width: '100%',
        height: '100%',
    },
    
});

export default Loading;