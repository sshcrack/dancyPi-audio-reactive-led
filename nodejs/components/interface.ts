export interface AvailableData {
    filters: Filter[];
    modes:   Mode[];
}

export interface Filter {
    name: string;
    vars: FilterVar[];
}

export interface FilterVar {
    type: string;
    name: string;
}

export interface Mode {
    name: string;
    vars: ModeVar[];
}

export interface ModeVar {
    min?: number;
    type: string;
    name: string;
}
