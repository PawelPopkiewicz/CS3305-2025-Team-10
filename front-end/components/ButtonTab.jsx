import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Button, Icon } from 'react-native-elements';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';

const ButtonList = () => {


    return (
        <View style={styles.container}>
            <Button
                // title="bus"
                icon={<Icon name="bus" type="font-awesome" />}
                buttonStyle={styles.button}
                // titleStyle={styles.title}
                iconContainerStyle={{ marginBottom: 5 }} // Space between icon and text
                onPress={() => router.push("/")}
            >
                <Text>

                </Text>
            </Button>

            <Button
                title="map"
                icon={<Icon name="map" type="font-awesome" />}
                buttonStyle={styles.button}
                titleStyle={styles.title}
                iconContainerStyle={{ marginBottom: 5 }} // Space between icon and text
                onPress={() => router.push("/screens/map")}
            />
        </View>
    );
};


const styles = StyleSheet.create({
    container: {
        width: '100%',
        height: 88,
        flexDirection: "row",
        flex: 1,
        justifyContent: 'flex-end',
        // alignItems: 'center',
    },
    button: {
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
        flexDirection: 'column', // Stack icon and text vertically
        // padding: 20,
    },
    title: {
        fontSize: fonts.body,
        marginTop: 5,
        color: colors.textSecondary
    },
});

export default ButtonList;