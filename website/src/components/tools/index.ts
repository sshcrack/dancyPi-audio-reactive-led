export function capitalizeWord(str: string) {
    const split = str.split("")
    const first = split.shift()?.toUpperCase() ?? ""

    return [ first, ...split ].join("")
}

export function rgbToHex(red: number, green: number, blue: number) {
    const rgb = (red << 16) | (green << 8) | (blue << 0);
    return '#' + (0x1000000 + rgb).toString(16).slice(1);
}

export function hexToRgb(hex: string) {
    const normal = hex.match(/^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i);
    if (normal) return normal.slice(1).map(e => parseInt(e, 16));

    const shorthand = hex.match(/^#([0-9a-f])([0-9a-f])([0-9a-f])$/i);
    if (shorthand) return shorthand.slice(1).map(e => 0x11 * parseInt(e, 16));

    return null;
}

export function getBaseUrl(location: Location) {
    const { protocol, host } = location
    return `${protocol}//${host/*"10.6.0.1:6789"*/}`
  }