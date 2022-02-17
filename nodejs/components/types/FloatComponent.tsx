import { VarProps } from '../interface';
import NumberSlider from './NumberSlider';

export default function IntComponent({ curr, onChange, variable }: VarProps<number>) {
    return <NumberSlider curr={curr} onChange={onChange} variable={variable} step={.1}></NumberSlider>
}