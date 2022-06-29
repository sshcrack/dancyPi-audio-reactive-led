export type DeviceList = {
    [key: string]: DeviceConfig
}

export interface DeviceConfig {
    name:   string;
    device: Device;
    config: Config;
}

export interface Config {
    speed:                  number;
    multiplier:             number;
    mode:                   string;
    filter_mode:            string;
    energy_brightness:      boolean;
    energy_brightness_mult: number;
    energy_speed:           boolean;
    energy_speed_mult:      number;
    energy_curr:            number;
    energy_sensitivity:     number;
    enabled:                boolean;
    locked:                 boolean;
    stack_concurrent:       number;
    stack_speed:            number;
    scanner_size:           number;
    scanner_shadow:         number;
    rainbow_speed:          number;
    rainbow_resolution:     number;
    energy_mirror:          boolean;
    shelf_animator_speed:   number;
    scanner_speed:          number;
}

export interface Device {
    DEVICE:                    string;
    N_PIXELS:                  number;
    SOFTWARE_GAMMA_CORRECTION: boolean;
    CONTROLLER:                string;
    UDP_PORT?:                  number;
    UDP_IP?:                    string;
}
