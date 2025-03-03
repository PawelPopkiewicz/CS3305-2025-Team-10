import {SafeAreaView, StyleSheet, Text, View, ScrollView, Platform, StatusBar} from "react-native";

import ButtonStop from "@/components/ButtonStop";
import ButtonBus from "@/components/ButtonBus";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";

export default function Index() {

    // const bus = [
    //     { id: 1, code: '2232', name: 'University College, Cork', arrival: '14:32' },
    //     { id: 2, code: '7890', name: 'City Centre, Cork', arrival: '15:45' },
    //     { id: 3, code: '4567', name: 'Kent Station, Cork', arrival: '15:00' }
    // ]

    return (

        <SafeAreaView
            style={styles.background}
        >
            <View style={styles.favourite}>
                <View style={styles.heading}>
                    <Text style={styles.textPrimary}>Favourite stops</Text>
                </View>
                {/* to be made functional once we store favourites*/}
                <ScrollView>
                    <ButtonStop />
                </ScrollView>

            </View>

            <View style={styles.favourite}>
                <View style={styles.heading}>
                    <Text style={styles.textPrimary}>Favourite buses</Text>
                </View>
                {/* to be made functional once we store favourites*/}
                <ScrollView>
                    <ButtonBus />
                </ScrollView>

            </View>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    background: {
        paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
        flex: 1,
        backgroundColor: colors.backgroundPrimary,
    },
    tab: {
        flex: 1,
        justifyContent: "flex-end",
    },
    favourite: {
        height: 200,
        backgroundColor: colors.backgroundPrimary,
    },
    heading: {
        borderTopLeftRadius: 17,
        borderBottomLeftRadius: 17,
        paddingLeft: 7,
        backgroundColor: colors.backgroundSecondary,
        fontSize: fonts.heading,
    },
    buttons: {
        marginTop: 5,
        color: colors.textSecondary,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    textPrimary: {
        padding: 7,
        textAlign: 'left',
        fontSize: fonts.heading,
        color: colors.textPrimary
    }
});