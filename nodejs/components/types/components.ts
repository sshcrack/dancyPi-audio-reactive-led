import { VarProps } from '../interface';
import FloatComponent from './FloatComponent';
import GradientComponent from './GradientComponent';
import IntComponent from './IntComponent';

export const typeComponents = {
    gradient: GradientComponent,
    float: FloatComponent,
    int: IntComponent
}

export type ComponentTypes = keyof typeof typeComponents;