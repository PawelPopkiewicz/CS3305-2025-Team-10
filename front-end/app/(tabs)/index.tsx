import {SafeAreaView, StyleSheet, Text, View, ScrollView, Platform} from "react-native";
import ButtonList from "@/components/ButtonList";
import ButtonBus from "@/components/ButtonBus";

import colors from "@/config/Colors";
import fonts from "@/config/Fonts";

export default function Index() {
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
                <ButtonList buttonData= {[
                    { id: '1', title: 'Stop 2232, University College Cork'},
                    { id: '2', title: 'Stop 2154, Patrick Street Cork'},
                    { id: '3', title: 'Stop 0026, North Mall, Cork'},
                    { id: '4', title: 'Stop 5682, Oliver Street, Cork'},
                    ]}/>
            </ScrollView>

        </View>

        <View style={styles.favourite}>
            <View style={styles.heading}>
                <Text style={styles.textPrimary}>Favourite buses</Text>
            </View>
            {/* to be made functional once we store favourites*/}
            <ScrollView>
                <ButtonBus buttonData= {[
                    { id: '3', title: 'Bus 220, Carrigaline - Crosshaven' },
                    ]}/>
            </ScrollView>

        </View>
    </SafeAreaView>
);
}

const styles = StyleSheet.create({
    background: {
        paddingTop: Platform.OS === 'android' ? 20 : 0,
        // paddingTop: 20,
        flex: 1,
        // justifyContent: 'flex-end',
        backgroundColor: colors.backgroundPrimary,
    },
    tab: {
        flex: 1,
        justifyContent: "flex-end",
    },
    favourite: {
        // padding: 7,
        // flex: 1,
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