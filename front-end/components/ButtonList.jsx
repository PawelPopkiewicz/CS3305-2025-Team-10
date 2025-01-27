import React from 'react';
import { View, ScrollView, Button, StyleSheet } from 'react-native';

const ButtonList = ({buttonData}) => {

    const handlePress = (title) => {
        alert(`You pressed ${title}`);
    };

    return (
        <ScrollView>
            {buttonData.map((item) => (
                <View key={item.id} style={styles.buttonContainer}>
                    <Button title={item.title} onPress={() => handlePress(item.title)} />
                </View>
            ))}
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    buttonContainer: {
        marginVertical: 10,
    },
});

export default ButtonList;