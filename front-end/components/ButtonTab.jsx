import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Button, Icon } from 'react-native-elements';
import {router} from 'expo-router';

const ButtonList = () => {


    return (
        <View style={styles.container}>
            <Button
                title="bus"
                icon={<Icon name="bus" type="font-awesome" />}
                buttonStyle={styles.button}
                titleStyle={styles.title}
                iconContainerStyle={{ marginBottom: 5 }} // Space between icon and text
                onPress={() => router.push("/")}
            />
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
        flexDirection: "row",
        justifyContent: 'center',
        alignItems: 'center',
    },
    button: {
        backgroundColor: '#007BFF',
        flexDirection: 'column', // Stack icon and text vertically
        padding: 20,
    },
    title: {
        fontSize: 16,
        marginTop: 5,
    },
});

export default ButtonList;