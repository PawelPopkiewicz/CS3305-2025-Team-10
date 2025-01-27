import {FlatList, StyleSheet, Text, TextInput, View} from "react-native";
import ButtonTab from "../../components/ButtonTab";
import {SetStateAction, useState} from "react";


export default function Map() {
    const data = ['220', 'WGB stop', 'Cherry', 'Date', 'Elderberry', 'Fig', 'Grape'];
    const [searchQuery, setSearchQuery] = useState('');
    const [filteredData, setFilteredData] = useState(data);

    const handleSearch = (query: SetStateAction<string>) => {
        setSearchQuery(query);
        if (query) {
            const filtered = data.filter(item => item.toLowerCase().includes(searchQuery.toLowerCase()));
            setFilteredData(filtered);
        } else {
            setFilteredData(data);
        }
    };

    return (
        <View style={styles.container}>
            <TextInput defaultValue={searchQuery} onChangeText={handleSearch} />
            <FlatList
                data={filteredData}
                keyExtractor={(item) => item}
            renderItem={({ item }) => (<Text>{item}</Text>)}/>
            <ButtonTab />
        </View>
    )
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
    }
})