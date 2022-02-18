import { Flex, NumberDecrementStepper, NumberIncrementStepper, NumberInput, NumberInputField, NumberInputStepper } from '@chakra-ui/react';
import { useState } from 'react';
import { VarProps } from '../interface';
import GeneralSlider from '../slider/GeneralSlider';

export default function GeneralNumber({ curr, onChange, variable, step, disabled = false, float }: NumberSliderProps) {
    const { min, max, sug_min, sug_max } = variable
    const [ emptied, setEmptied ] = useState(false)

    const onChangeLocal = (e: string) => {
        if(e.trim().length !== 0)
            setEmptied(false)

        if (isNaN(e as any) || e.trim().length === 0) {
            setEmptied(true)
            return
        }

        onChange(float ? parseFloat(e) : parseInt(e))
    }

    const totalMin = sug_min ?? min
    const totalMax = sug_max ?? max
    const isInvalid = min ? curr < min : false || max ? curr > max : false
    if(min && curr < min)
        onChange(min)

    if(max && curr > max)
        onChange(max)

    return <Flex w='100%'>
        <NumberInput
            onChange={onChangeLocal}
            value={emptied ? "" : curr}
            min={totalMin}
            max={totalMax}
            maxW='100px'
            mr='2rem'
            step={step}
            isDisabled={disabled}
            isInvalid={isInvalid}
        >
            <NumberInputField />
            <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
            </NumberInputStepper>
        </NumberInput>
        <GeneralSlider
            curr={curr}
            onChange={onChange}
            variable={variable}
            step={step}
            disabled={disabled}
        />
    </Flex>
}

export type NumberSliderProps = VarProps<number> & {
    step?: number,
    disabled?: boolean,
    float: boolean
}