import {Button} from 'react-native';
import {useState} from "react";

export default function CounterButton () {
    const [ButtonCounter, setButtonCounter] = useState(1);
    return (
            <Button title=  {"Button Title " + ButtonCounter}  onPress={() => {setButtonCounter(ButtonCounter+1)}} />
    )
}