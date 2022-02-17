import { VarProps } from '../interface';
import { NumberInput, NumberInputField, NumberDecrementStepper, NumberInputStepper, NumberIncrementStepper, Flex, Slider, SliderTrack, SliderFilledTrack, SliderThumb } from '@chakra-ui/react';

export default function NumberSlider({ curr, onChange, variable, step}: NumberSliderProps) {
    const { min, max, sug_min, sug_max} = variable

    const onChangeLocal = (e: string | number) => {
        if (isNaN(e as any))
            return

        onChange(typeof e === "string" ? parseInt(e) : e)
    }

    const totalMin = sug_min ?? min
    const totalMax = sug_max ?? max

    return <Flex w='100%'>
        <NumberInput onChange={onChangeLocal} value={curr} min={totalMin} max={totalMax} maxW='100px' mr='2rem' step={step}>
            <NumberInputField />
            <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
            </NumberInputStepper>
        </NumberInput>
        <Slider
            flex='1'
            focusThumbOnChange={false}
            value={curr}
            onChange={onChangeLocal}
            min={totalMin}
            max={totalMax}
            step={step}
        >
            <SliderTrack>
                <SliderFilledTrack />
            </SliderTrack>
            <SliderThumb fontSize='sm' boxSize='32px'>{curr}</SliderThumb>
        </Slider>
    </Flex>
}

export type NumberSliderProps = VarProps<number> & {
    step?: number
}