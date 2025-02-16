import {FlatList, StyleSheet, Text, TextInput, View} from "react-native";
import {SetStateAction, useState} from "react";

const TransitFilter = () => {
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
            <TextInput defaultValue={searchQuery} onChangeText={handleSearch}/>
            <FlatList
                data={filteredData}
                keyExtractor={(item) => item}
                renderItem={({item}) => (<Text>{item}</Text>)}/>
        </View>
    )
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
    }
})
export default TransitFilter;