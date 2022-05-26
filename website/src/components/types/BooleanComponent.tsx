import { VarProps } from '../interface';
import { Switch } from "@chakra-ui/react"

export default function BooleanComponent({ curr, onChange, variable }: VarProps<boolean>) {
    return <Switch checked={curr} onChange={e => onChange(e.target.checked)} />
}