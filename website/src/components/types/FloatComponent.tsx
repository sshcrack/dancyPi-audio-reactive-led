import { VarProps } from '../interface';
import GeneralNumber from './GeneralNumber';

export default function FloatComponent({ curr, onChange, variable }: VarProps<number>) {
    return <GeneralNumber curr={curr} onChange={onChange} variable={variable} step={.1} float={true}></GeneralNumber>
}