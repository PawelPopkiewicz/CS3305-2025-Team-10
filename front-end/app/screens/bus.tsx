import {Text, View, StyleSheet, SafeAreaView, Platform} from "react-native";
import {Button, Icon} from 'react-native-elements';
import {router} from 'expo-router';
import FontAwesomeIcon from "react-native-vector-icons";

import ButtonList from "@/components/ButtonList";
import ButtonTab from "@/components/ButtonTab";
import colors from "@/config/Colors";
import fonts from "@/config/Fonts";

export default function Bus() {
return (
    <SafeAreaView
        style={styles.background}
    >
        {/* Chosen bus */}
        <View style={styles.bus}>
            <Button
                icon={<Icon iconStyle={styles.icon} name="chevron-left" type="font-awesome"/>}
                buttonStyle={styles.button}
                onPress={() => router.push("/")}
                >
            </Button>

            <View style={styles.route}>
                <Text style={styles.textPrimary}>220</Text>
            </View>

            <View style={styles.heading}>
                <Text style={styles.textPrimary}>Carrigaline-Crosshaven</Text>
            </View>

            {/* to be made functional once we store favourites */}
            <Button                
                icon={<Icon iconStyle={styles.icon} name="star" type="font-awesome"/>}
                buttonStyle={styles.button}
                onPress={() => alert("favs")}
            >
            </Button>

        </View>

        {/* See on the map part */}
        <View style={styles.map}>
            <Text style={styles.heading}>See on the map</Text>
            
            {/* Return map page with selected bus route highlighted */}
            <Button                
                icon={<Icon iconStyle={styles.icon} name="arrow-right" type="font-awesome"/>}
                buttonStyle={styles.button}
                onPress={() => router.push('/screens/map')}
            >
            </Button>
        </View>

        {/* Display each bus stop of selected bus ordered by arrival time, make scrollView, bare bones given below */}
        
        <View style={styles.stop}>
            {/* Ideally, make arrows change colors depending if the bus visited the stop yet or not */}
            <Icon iconStyle={styles.busPathVisited} name="arrow-down" type="font-awesome"/>
            <Text style={styles.textSecondary}>Stop 2232 University College, Cork</Text>
            <Text style={styles.textSecondary}>14:32</Text>
        </View>

        <View style={styles.stop}>
            <Icon iconStyle={styles.busPathNotVisited} name="arrow-down" type="font-awesome"/>
            <Text style={styles.textSecondary}>Stop 2238 Patrick Street, Cork</Text>
            <Text style={styles.textSecondary}>14:44</Text>
        </View>

        <ButtonTab />
    </SafeAreaView>
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
    bus: {
        flexDirection: 'row',
        height: '10%',
        width: '100%',
        backgroundColor: colors.backgroundPrimary,
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    route: {
        backgroundColor: colors.backgroundSecondary,
        color: colors.textPrimary,
        flexGrow: 1,
        fontSize: fonts.heading,
    },
    heading: {
        color: colors.textPrimary,
        flexGrow: 3,
        flexDirection: 'column',
        fontSize: fonts.heading,
    },
    button: {
        flexGrow: 1,
        color: colors.backgroundPrimary,
        backgroundColor: colors.backgroundPrimary,
    },
    icon: {
        color: colors.textPrimary,
    },
    map: {
        flexDirection: 'row',
        height: '10%',
        width: '100%',
        borderBottomWidth: 1,
        borderBottomColor: colors.border,
    },
    busPathVisited: {
        // transform: [{rotate: "80deg"}],
        color: colors.objectSelected,
    },
    busPathNotVisited: {
        color: colors.objectNotSelected,
    },
    textPrimary: {
        padding: 7,
        textAlign: 'left',
        fontSize: fonts.heading,
        color: colors.textPrimary
    },
    textSecondary: {
        color: colors.textPrimary,
        fontSize: fonts.subHeading,
    },
    textDescription: {
        color: colors.textSecondary,
        fontSize: fonts.body,
    },
    description: {
        justifyContent: 'space-evenly',
        flexDirection: 'row',
    },
    stop: {
        justifyContent: 'space-evenly',
        flexDirection: 'row', 
    }
});