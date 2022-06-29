import { Flex, Spinner, Switch, Text } from '@chakra-ui/react';
import { ChangeEvent, Dispatch, SetStateAction } from "react";
import { DeviceList } from '../interfaces/DeviceList';
import { getBaseUrl } from './tools';

export default function ToggleEverything({ deviceList, setUpdate }: { deviceList: DeviceList, setUpdate: Dispatch<SetStateAction<number>> }) {
    if (!deviceList)
        return <Spinner />


    const everythingEnabled = Object.values(deviceList).every(({ config }) => config.enabled);

    const onSwitchChange =async (e: ChangeEvent<HTMLInputElement>) => {
        const base = getBaseUrl(window.location)
        const enabled = e.target.checked
        await fetch(`${base}/allenabled?enabled=${enabled}`)
        setUpdate(Math.random())
    }
    return <Flex justifyContent='center' alignItems='center'>
        <Text mr='5'>Everything enabled:</Text>
        <Switch isChecked={everythingEnabled} onChange={e => onSwitchChange(e)}/>
    </Flex>
}