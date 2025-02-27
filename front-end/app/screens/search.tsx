import {Platform, SafeAreaView, ScrollView, StyleSheet, Text, TouchableOpacity, View, StatusBar, FlatList} from "react-native";
import {Icon, Input} from '@rneui/themed';
import React, {useState, useRef, useEffect} from "react";
import {router} from "expo-router";


import ButtonStop from "@/components/ButtonStop";
import ButtonBus from "@/components/ButtonBus";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {useBusData} from "@/hooks/useBusData";
import {Stop} from "@/types/stop";
import {Bus} from "@/types/bus";

export default function Search() {

    const [selected, setSelected] = useState(null);
    const changeFilter = (filter) => {
        setSelected(filter);
    };


    const { stops } = useBusData();
    const [query, setQuery] = useState("");
    const [filteredStops, setFilteredStops] = useState(stops);
    const inputRef = useRef(null);

    const handleSearch = (text: string) => {
        setQuery(text);
        if (text.length > 0) {
            const results = stops.filter((stop) =>
                stop.name.toLowerCase().includes(text.toLowerCase()) ||
                stop.code.toLowerCase().includes(text.toLowerCase())
            );
            setFilteredStops(results);
        } else {
            setFilteredStops(stops); // Show all stops when input is empty
        }
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            if (inputRef.current) {
                // @ts-ignore
                inputRef.current.focus(); // Automatically focus input
            }
        }, 100);

        return () => clearTimeout(timer);
    }, []);

    return (

        <SafeAreaView style={styles.background}>

            {/* input field */}
            <Input
            ref={inputRef}
            inputStyle={styles.textPrimary}
            inputContainerStyle={styles.input}
            value={query} // Controlled input
            onChangeText={handleSearch} // Update state on change
            placeholder="Search bus stop or route"
            rightIcon={<Icon iconStyle={styles.clear} onPress={() => handleSearch("")} name="plus" type="font-awesome"/>}    // clean input
            leftIcon={<Icon iconStyle={styles.back} onPress={() => router.back()} name="chevron-left"       // go back
                            type="font-awesome"/>}
            >
            </Input>

            <View style={styles.filters}>

                {/* bus filter button */}
                <TouchableOpacity
                style={[styles.filter, {backgroundColor: selected === "Bus" ? colors.backgroundSecondary : colors.backgroundPrimary},]}
                onPress={() => changeFilter("Bus")} 
                activeOpacity={0.1}
                >
                    <View>
                        <Text style={[{color: selected === "Bus" ? colors.objectSelected : colors.textSecondary}]}>
                            Bus
                        </Text>
                    </View>
                </TouchableOpacity>

                {/* stop filter button */}
                <TouchableOpacity
                style={[styles.filter, {backgroundColor: selected === "Stop" ? colors.backgroundSecondary : colors.backgroundPrimary},]}
                onPress={() => changeFilter("Stop")} 
                activeOpacity={0.1}
                >
                    <View>
                        <Text style={[{color: selected === "Stop" ? colors.objectSelected : colors.textSecondary}]}>
                            Stop
                        </Text>
                    </View>
                </TouchableOpacity>
            </View>

            {/* List of filtered stops */}
            <FlatList
                data={filteredStops}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <TouchableOpacity onPress={() => setQuery(item.name)}>
                        <Text>{item.name} ({item.code})</Text>
                    </TouchableOpacity>
                )}
            />

            

            {/* Display buses and stops based on search here */}
            {/* <ScrollView>
                <ButtonBus />
                <ButtonStop />

            </ScrollView> */}

        </SafeAreaView >


    );
}

const styles = StyleSheet.create({
    background: {
        paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
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
    filter: {
        padding: 7,
        paddingHorizontal: 30,
        borderWidth: 1,
        borderRadius: 17,
        borderColor: colors.border,
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