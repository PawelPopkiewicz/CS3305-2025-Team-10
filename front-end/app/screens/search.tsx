import { Platform, SafeAreaView, FlatList, StyleSheet, Text, TouchableOpacity, View, StatusBar } from "react-native";
import { Icon, Input } from "@rneui/themed";
import React, { useState, useRef, useEffect } from "react";
import { router } from "expo-router";

import SearchButtonStop from "@/components/SearchButtonStop";
import SearchButtonBus from "@/components/SearchButtonBus";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";
import { Stop } from "@/types/stop";
import { Bus } from "@/types/bus";
import {useSelector} from "react-redux";
import {RootState} from "@/app/redux/store";

export default function Search() {

    const stops = useSelector((state: RootState) => state.stop.stops);
    const buses = useSelector((state: RootState) => state.bus.buses);

    const [selected, setSelected] = useState<"Stop" | "Bus">("Stop"); // Default to Stop
    const [query, setQuery] = useState("");
    const [filteredResults, setFilteredResults] = useState<(Bus | Stop)[]>(stops); // Fix here
    const inputRef = useRef(null);

    const changeFilter = (filter: "Stop" | "Bus") => {
        setSelected(filter);
        setQuery("");
        setFilteredResults(filter === "Bus" ? buses : stops);
        if (filter === "Bus") {
            console.log("Buses when Bus filter selected:", buses);
        } else {
            console.log("Stops when Stop filter selected:", stops);
        }
    };

    const handleSearch = (text: string) => {
        setQuery(text);
        const lowerText = text.toLowerCase().trim(); // Convert input to lowercase & remove extra spaces

        if (text.length > 0) {
            if (selected === "Stop") {
                setFilteredResults(stops.filter((stop) =>
                    stop.name.toLowerCase().includes(text.toLowerCase()) ||
                    stop.code.toLowerCase().includes(text.toLowerCase())
                ));
            } else {
                setFilteredResults(buses.filter((bus) =>
                    bus.route.toLowerCase().trim() === lowerText || // Exact match for route
                    bus.route.toLowerCase().includes(lowerText) || // Partial match for route
                    bus.headsign.toLowerCase().trim() === lowerText || // Exact match for headsign
                    bus.headsign.toLowerCase().includes(lowerText) // Partial match for headsign
                ));
                
            }
        } else {
            setFilteredResults(selected === "Bus" ? buses : stops);
        }
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            if (inputRef.current) {
                // @ts-ignore
                inputRef.current.focus();
            }
        }, 100);
        return () => clearTimeout(timer);
    }, []);

    return (
        <SafeAreaView style={styles.background}>
            {/* Input Field */}
            <Input
                ref={inputRef}
                inputStyle={styles.textPrimary}
                inputContainerStyle={styles.input}
                value={query}
                onChangeText={handleSearch}
                placeholder={`Search ${selected === "Bus" ? "bus route or headsign" : "bus stop or code"}`}
                rightIcon={<Icon iconStyle={styles.clear} onPress={() => handleSearch("")} name="plus" type="font-awesome" />}
                leftIcon={<Icon iconStyle={styles.back} onPress={() => router.back()} name="chevron-left" type="font-awesome" />}
            />

            {/* Filter Buttons */}
            <View style={styles.filters}>
                <TouchableOpacity
                    style={[styles.filter, { backgroundColor: selected === "Bus" ? colors.backgroundSecondary : colors.backgroundPrimary }]}
                    onPress={() => changeFilter("Bus")}
                    activeOpacity={0.1}
                >
                    <Text style={{ color: selected === "Bus" ? colors.objectSelected : colors.textSecondary }}>Bus</Text>
                </TouchableOpacity>

                <TouchableOpacity
                    style={[styles.filter, { backgroundColor: selected === "Stop" ? colors.backgroundSecondary : colors.backgroundPrimary }]}
                    onPress={() => changeFilter("Stop")}
                    activeOpacity={0.1}
                >
                    <Text style={{ color: selected === "Stop" ? colors.objectSelected : colors.textSecondary }}>Stop</Text>
                </TouchableOpacity>
            </View>

            {/* Filtered List */}
            <FlatList
                data={filteredResults}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) =>
                    selected === "Bus" ? <SearchButtonBus item={item as Bus} /> : <SearchButtonStop item={item as Stop} />
                }
            />
        </SafeAreaView>
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