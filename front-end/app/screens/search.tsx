import {Text, View, StyleSheet, TouchableOpacity} from "react-native";
import { Input, Icon } from '@rneui/themed';
import React, { useRef, useState } from "react";
import { router } from "expo-router";
import {Button} from 'react-native-elements';

import ButtonList from "@/components/ButtonList";
import ButtonTab from "@/components/ButtonTab";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";



export default function Search() {
    // const inputRef = useRef(null);

    // const clearText = () => {
    //     if (inputRef.current) {
    //         inputRef.current.clear(); // Clears the input field
    //     }
    // };

    const [text, setText] = useState("");

    return (
        <View style={styles.background}>

            <Input
            value={text} // Controlled input
            onChangeText={setText} // Update state on change
            placeholder="Search bus stop or route"
            rightIcon={<Icon iconStyle={styles.clear} onPress={() => setText("")} name="plus" type="font-awesome"/>}
            leftIcon={<Icon iconStyle={styles.back} onPress={() => router.push('/')} name="chevron-left" type="font-awesome"/>}
            >
            </Input>

            <View style={styles.filters}>

                <TouchableOpacity
                style={styles.filterNotSelected}
                // {/* onPress={() => handlePress(item.title)} */}
                activeOpacity={0.1}
                >
                    <View>
                        <Text style={styles.textSecondary}>
                            Bus
                        </Text>
                    </View>
                </TouchableOpacity>

                <TouchableOpacity
                style={styles.filterSelected}
                // {/* onPress={() => handlePress(item.title)} */}
                activeOpacity={0.1}
                >
                    <View>
                        <Text style={styles.textSelected}>
                            Stop
                        </Text>
                    </View>
                </TouchableOpacity>
            </View>
        </View >


    );
}

const styles = StyleSheet.create({
    background: {
        // paddingTop: Platform.OS === 'android' ? 20 : 0,
        paddingTop: 20,
        flex: 1,
        // justifyContent: 'flex-end',
        backgroundColor: colors.backgroundPrimary,
        // height: '100%'
    },
    clear: {
        color: colors.textPrimary,
        transform: [{rotate: "45deg"}],
    },
    back: {
        color: colors.textPrimary
    },
    filters: {
        flexDirection: 'row',
        justifyContent: 'space-evenly',
    },
    filterNotSelected: {
        borderWidth: 1,
        borderRadius: 17,
        borderColor: colors.border,
        backgroundColor: colors.backgroundPrimary,
    },
    filterSelected: {
        borderWidth: 1,
        borderColor: colors.border,
        borderRadius: 17,
        backgroundColor: colors.backgroundSecondary,
    },
    textSelected: {
        color: colors.objectSelected,
        fontSize: fonts.subHeading
    },
    textPrimary:{
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    textSecondary: {
        color: colors.textSecondary,
        fontSize: fonts.body,
    },
});