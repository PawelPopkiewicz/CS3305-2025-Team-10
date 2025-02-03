import React from 'react';
import {StyleSheet, View} from 'react-native';
import {Button, Icon} from 'react-native-elements';
import {router} from 'expo-router';

import colors from '@/config/Colors';
import fonts from '@/config/Fonts';

const ButtonList = () => {


    return (
        <View style={styles.container}>
            <Button
                title="bus"
                icon={<Icon iconStyle={styles.icon} name="bus" type="font-awesome"/>}
                buttonStyle={styles.button}
                titleStyle={styles.title}
                iconContainerStyle={{marginBottom: 5}} // Space between icon and text
                onPress={() => router.push("/")}
            >
                {/* <Text>

                </Text> */}
            </Button>

            <Button
                title="map"
                icon={<Icon iconStyle={styles.icon} name="map" type="font-awesome"/>}
                buttonStyle={styles.button}
                titleStyle={styles.title}
                iconContainerStyle={{marginBottom: 5}} // Space between icon and text
                onPress={() => router.push("/screens/map")}
            />
        </View>
    );
};


const styles = StyleSheet.create({
    container: {
        borderTopColor: colors.border,
        borderWidth: 1,
        // width: '100%',
        // height: '10%',
        flexDirection: "row",
        // flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        alignContent: "space-between",
        columnGap: 500,
        // top: 400,        //display depending on size of device?
        
    },
    button: {
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
        flexDirection: 'column', // Stack icon and text vertically
        padding: 20,
    },
    title: {
        fontSize: fonts.body,
        marginTop: 5,
        color: colors.textSecondary
    },
    icon: {
        color: colors.textPrimary,
    },
});

export default ButtonList;