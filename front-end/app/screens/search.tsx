import {Button, Text, View} from "react-native";
import ButtonList from "@/components/ButtonList";
import ButtonTab from "@/components/ButtonTab";

export default function Search({navigation}) {
return (
    <View
        style={{
            flex: 1,
            justifyContent: "center",
            alignItems: "center",
        }}
    >
        <Text>Favourite stops</Text>
        {/* to be made functional once we store favourites*/}
        <ButtonList buttonData= {[
            { id: '1', title: 'Button 1' },
            { id: '2', title: 'Button 2' }]}/>
        <Text>Favourite buses</Text>
        <ButtonList buttonData= {[
            { id: '1', title: 'Button 1' },
            { id: '2', title: 'Button 2' }]}/>

        <ButtonTab />


        <Button title="Go Back" onPress={() => navigation.goBack()} />
    </View>
);
}