import React from 'react';
import {ActivityIndicator, StyleSheet, Text, TouchableOpacity, View} from 'react-native';
import {router} from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';


const ErrorData = ({ text }: { text: String }) => {
    return (
        <SafeAreaView style={styles.backGround}>
                <Text style={styles.textData}>{text}</Text>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    textData: {
        color: colors.textPrimary,
        textAlign: "center",
        fontSize: 24,
    },
    backGround: {
        backgroundColor: colors.backgroundPrimary,
        textAlign: "center",
        justifyContent: 'center',
        alignContent: 'center',
        width: '100%',
        height: '100%',
    },
    
});

export default ErrorData;