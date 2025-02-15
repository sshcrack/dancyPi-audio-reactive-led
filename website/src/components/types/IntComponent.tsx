import { VarProps } from '../interface';
import GeneralNumber from './GeneralNumber';

export default function IntComponent({ curr, onChange, variable }: VarProps<number>) {
    return <GeneralNumber curr={curr} onChange={onChange} variable={variable} step={1} float={false} />
}