export interface AvailableData {
    filters: General[];
    modes: General[];
}

export interface General {
    name: string;
    vars: Var[];
}


export interface Var {
    min?: number;
    max?: number;
    type: string;
    name: string;
    sug_min?: number;
    sug_max?: number;
}

export interface VarProps<T> {
    variable: Var
    onChange: (value: T) => void
    curr: T
}

export type StoredData = NormalStorageKeys & {
    [key: string]: any
}

export interface NormalStorageKeys {
    mode: string;
    filter_mode: string;
    speed: number;
    multiplier: number;
    energy_brightness: boolean;
    energy_brightness_mult: number;
    energy_speed: boolean;
    energy_speed_mult: number;
    energy_sensitivity: number;
}