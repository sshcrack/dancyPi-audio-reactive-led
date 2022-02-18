import { Slider, SliderFilledTrack, SliderThumb, SliderTrack } from '@chakra-ui/react';
import { NumberSliderProps } from '../types/GeneralNumber';

export default function GeneralSlider({ curr, onChange, variable, step, disabled=false }: GeneralSliderProps) {
    const { min, max, sug_min, sug_max} = variable
    const totalMin = sug_min ?? min
    const totalMax = sug_max ?? max

    return <Slider
        flex='1'
        focusThumbOnChange={false}
        value={curr}
        onChange={onChange}
        min={totalMin}
        max={totalMax}
        step={step}
        isDisabled={disabled}
    >
        <SliderTrack>
            <SliderFilledTrack />
        </SliderTrack>
        <SliderThumb fontSize='sm' boxSize='32px'>{curr}</SliderThumb>
    </Slider>
}

type GeneralSliderProps = Omit<NumberSliderProps, "float">