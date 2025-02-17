import {ScrollView, StyleSheet, Text, TouchableOpacity, View} from "react-native";
import {Icon, Input} from '@rneui/themed';
import React, {useState, useRef, useEffect} from "react";
import {router} from "expo-router";

import ButtonList from "@/components/ButtonList";
import ButtonBus from "@/components/ButtonBus";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";


export default function Search() {

    const [text, setText] = useState("");
    const inputRef = useRef(null);

    useEffect(() => {
        const timer = setTimeout(() => {
          if (inputRef.current) {
            inputRef.current.focus(); // Open keyboard automatically
          }
        }, 100); // Delay ensures the UI is ready
    
        return () => clearTimeout(timer);
      }, []);
    return (
        <View style={styles.background}>

            <Input
            ref={inputRef}
            inputStyle={styles.textPrimary}
            inputContainerStyle={styles.input}
            value={text} // Controlled input
            onChangeText={setText} // Update state on change
            placeholder="Search bus stop or route"
            rightIcon={<Icon iconStyle={styles.clear} onPress={() => setText("")} name="plus" type="font-awesome"/>}
            leftIcon={<Icon iconStyle={styles.back} onPress={() => router.back()} name="chevron-left"
                            type="font-awesome"/>}
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

            {/* Display buses and stops based on search here*/}
            <ScrollView style={styles.test}>
                <ButtonBus buttonData= {[
                    { id: '3', title: 'Bus 220, Carrigaline - Crosshaven' },
                    ]}/>
                <ButtonList buttonData={[
                    { id: '1', title: 'Stop 2232, University College Cork'},
                ]}/>
            </ScrollView>
        </View >


    );
}

const styles = StyleSheet.create({
    test: {
        // borderBottomWidth: 3,
        // borderBottomColor: colors.border,
    },
    background: {
        // paddingTop: Platform.OS === 'android' ? 20 : 0,
        paddingTop: 50,
        flex: 1,
        // justifyContent: 'flex-end',
        backgroundColor: colors.backgroundPrimary,
        // height: '100%'
    },
    input: {
        alignItems: "center",
        borderRadius: 30 ,
        borderWidth: 2,
        padding: 3,
        paddingHorizontal: 15,
        borderColor: colors.border,
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
        padding: 7,
        paddingHorizontal: 30,
        borderWidth: 1,
        borderRadius: 17,
        borderColor: colors.border,
        backgroundColor: colors.backgroundPrimary,
    },
    filterSelected: {
        padding: 7,
        paddingHorizontal: 30,
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