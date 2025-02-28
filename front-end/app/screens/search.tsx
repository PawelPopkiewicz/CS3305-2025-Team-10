import {Platform, SafeAreaView, ScrollView, StyleSheet, Text, TouchableOpacity, View, StatusBar, FlatList} from "react-native";
import {Icon, Input} from '@rneui/themed';
import React, {useState, useRef, useEffect} from "react";
import {router} from "expo-router";


import ButtonStop from "@/components/ButtonStop";
import ButtonBus from "@/components/ButtonBus";
import SearchButtonStop from "@/components/SearchButtonStop";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import {useBusData} from "@/hooks/useBusData";
import {Stop} from "@/types/stop";
import {Bus} from "@/types/bus";

export default function Search() {

    const [selected, setSelected] = useState<"Bus" | "Stop" | null>(null);
    const [query, setQuery] = useState<string>("");
    const [filteredResults, setFilteredResults] = useState<(Bus | Stop)[]>([]);
    const inputRef = useRef(null);

    // Access buses and stops from Redux
    const { buses, stops } = useBusData();

    // Type guards to check if an item is a Bus or a Stop
    const isStop = (item: any): item is Stop => "name" in item && "code" in item;
    const isBus = (item: any): item is Bus => "headsign" in item && "route" in item;

    // Function to filter search results based on query and selected filter
    const filterResults = (text: string, filter: "Bus" | "Stop" | null) => {
        let results: (Bus | Stop)[] = [];

        if (filter === "Bus") {
            results = buses;
        } else if (filter === "Stop") {
            results = stops;
        } else {
            results = [...buses, ...stops]; // Show both if no filter is selected
        }

        if (text.length > 0) {
            results = results.filter((item) => {
                if (isStop(item)) {
                    return item.name.toLowerCase().includes(text.toLowerCase()) ||
                           item.code.toLowerCase().includes(text.toLowerCase());
                } else if (isBus(item)) {
                    return item.headsign.toLowerCase().includes(text.toLowerCase()) ||
                           item.route.toLowerCase().includes(text.toLowerCase());
                }
                return false;
            });
        }

        setFilteredResults(results);
    };

    // Handle input changes
    const handleSearch = (text: string) => {
        setQuery(text);
        filterResults(text, selected);
    };

    // Handle filter selection
    const changeFilter = (filter: "Bus" | "Stop") => {
        setSelected(filter);
        filterResults(query, filter);
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
                data={filteredResults?.filter(item => item !== undefined) || []} // Ensure no undefined items
                keyExtractor={(item, index) => (item?.id ? item.id.toString() : `key-${index}`)}
                renderItem={({ item }) => item ? <SearchButtonStop item={item} /> : null}
                ListEmptyComponent={<Text>No results found</Text>}
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