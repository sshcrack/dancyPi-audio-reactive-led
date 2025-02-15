import { Box, Flex, Switch, Text } from '@chakra-ui/react';
import { ChangeEvent } from 'react';
import "../generalComp.css";
import { StoredData, Var } from './interface';
import { capitalizeWord } from './tools';
import GeneralNumber from './types/GeneralNumber';

export default function EnergyComp({ onChange, stored }: EnergyMeterProps) {
    const sensitivityVar: Var = {
        name: "energy_sensitivity",
        type: "float",
        max: .99,
        min: 0
    }

    const brightnessVar: Var = {
        ...sensitivityVar,
        name: "energy_brightness_mult",
        max: 10
    }

    const speedVar: Var = {
        ...sensitivityVar,
        max: 10,
        name: "energy_speed_mult"
    }

    const currSensitivity = stored[sensitivityVar.name]

    const updateStorage = (key: string, value: unknown) => {
        stored[key] = value
        onChange(stored)
    }

    const brightnessComps = genEnergySwitches(brightnessVar, "brightness", stored, onChange)
    const speedComps = genEnergySwitches(speedVar, "speed", stored, onChange)

    const bothDisabled = !(stored["energy_brightness"] || stored["energy_speed"])
    return <Flex flexDir='column' w='100%' justifyContent='center' alignItems='center'>
        <Flex w='100%' className='comp' justifyContent='center' alignItems='center'>
            <Flex flex='.4'>
                <Text>Sensitivity</Text>
            </Flex>
            <Flex className='compContainer'>
                <Switch opacity='0' size='lg' mr='2rem'/>
                <GeneralNumber
                    curr={currSensitivity}
                    onChange={numb => updateStorage(sensitivityVar.name, numb)}
                    step={.01}
                    variable={sensitivityVar}
                    float={true}
                    disabled={bothDisabled}
                />
            </Flex>
        </Flex>
        <Box mt='3em' />

        {brightnessComps}

        <Box mt='3em' />
        {speedComps}
    </Flex>
}

function genEnergySwitches(curr_var: Var, type: EnergyType, stored: StoredData, onChange: (data: StoredData) => void,) {
    const generalKey = "energy_" + type
    const multiplierKey = generalKey + "_mult"

    const currEnabled = stored[generalKey]
    const currMultiplier = stored[multiplierKey]

    const title = capitalizeWord(type)

    const onSwitchChange = (input: ChangeEvent<HTMLInputElement>) => {
        stored[generalKey] = input.target.checked
        onChange(stored)
    }

    const onMultiplierChange = (input: number) => {
        stored[multiplierKey] = input
        onChange(stored)
    }


    return <Flex className='comp' w='100%' justifyContent='center' alignItems='center'>
        <Flex flex='.4'>
            <Text>{title}</Text>
        </Flex>
        <Flex className='compContainer' alignItems='center'>
            <Switch
                variant='green'
                onChange={onSwitchChange}
                isChecked={currEnabled}
                mr='2rem'
                size='lg'
            />
            <GeneralNumber
                curr={currMultiplier}
                onChange={onMultiplierChange}
                variable={curr_var}
                disabled={!currEnabled}
                step={.1}
                float={true}
            ></GeneralNumber>
        </Flex>
    </Flex>
}

type EnergyType = "brightness" | "speed"

interface EnergyMeterProps {
    stored: StoredData;
    onChange: (data: StoredData) => void;
}