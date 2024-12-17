/**
 * Updates CSS variables on the document's root element based on the provided styles object.
 * 
 * @param styles - An object containing style properties and values.
 * @param prefix - An optional prefix to add to the CSS variable names.
 * 
 * @example
 * ```typescript
 * updateCSSVariables({ color_primary: '#ff0000', font_size: '16px' });
 * // Sets --color-primary: #ff0000 and --font-size: 16px on the document's root element.
 * ```
 */
export function updateCSSVariables(styles: object, prefix: string = ''): void {
    if (typeof document === 'undefined') return;

    for (const [key, value] of Object.entries(styles)) {
        if (typeof value === 'object' && value !== null) {
            updateCSSVariables(value, `${prefix}${key}-`);
        } else {
            const cssVarName = `--${prefix}${key.replace(/_/g, '-')}`;
            document.documentElement.style.setProperty(cssVarName, value);
        }
    }
}

/**
 * Converts a blob URL to a Base64-encoded string.
 * 
 * @param blobUrl - The URL of the blob to convert.
 * @returns A promise that resolves to the Base64-encoded string.
 * 
 * @example
 * ```typescript
 * const base64String = await convertBlobToBase64('blob:http://example.com/12345');
 * console.log(base64String); // data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...
 * ```
 */
export async function convertBlobToBase64(blobUrl: string): Promise<string> {
    try {
        const response = await fetch(blobUrl);
        if (!response.ok) {
            throw new Error(`Failed to fetch blob: ${response.statusText}`);
        }
        const blob = await response.blob();
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result as string);
            reader.onerror = () => reject('Error converting blob to Base64');
            reader.readAsDataURL(blob);
        });
    } catch (error) {
        console.error(error);
        return '';
    }
}

/**
 * Removes the percent sign from a string and converts it to a number.
 * 
 * @param value - The string containing a percentage value.
 * @returns The numeric value without the percent sign.
 * 
 * @example
 * ```typescript
 * const number = removePercent('50%');
 * console.log(number); // 50
 * ```
 */
export function removePercent(value: string): number {
    return parseFloat(value.replace('%', ''));
}

/**
 * Removes the degree sign from a string and converts it to a number.
 * 
 * @param value - The string containing a degree value.
 * @returns The numeric value without the degree sign.
 * 
 * @example
 * ```typescript
 * const number = removeDeg('180deg');
 * console.log(number); // 180
 * ```
 */
export function removeDeg(value: string): number {
    return parseFloat(value.replace('deg', ''));
}

/**
 * Converts RGB color values to an HSL string representation.
 * 
 * @param r - The red component, a number between 0 and 255.
 * @param g - The green component, a number between 0 and 255.
 * @param b - The blue component, a number between 0 and 255.
 * @returns An object with the HSL representation as strings with units.
 * 
 * @example
 * ```typescript
 * const hsl = RGBToHSLString(255, 0, 0);
 * console.log(hsl); // { h: '0deg', s: '100%', l: '50%' }
 * ```
 */
export function RGBToHSLString(r: number, g: number, b: number) {
    const out = RGBToHSL(r, g, b);
    return { h: `${out.h * 360}deg`, s: `${out.s * 100}%`, l: `${out.l * 100}%` };
}

/**
 * Converts HSL string values to RGB color values.
 * 
 * @param h - The hue as a string with a degree unit (e.g., '180deg').
 * @param s - The saturation as a string with a percent unit (e.g., '50%').
 * @param l - The lightness as a string with a percent unit (e.g., '50%').
 * @returns An object with the RGB representation, with each component (r, g, b) as a number between 0 and 255.
 * 
 * @example
 * ```typescript
 * const rgb = HSLStringToRGB('180deg', '50%', '50%');
 * console.log(rgb); // { r: 64, g: 191, b: 191 }
 * ```
 */
export function HSLStringToRGB(h: string, s: string, l: string) {
    return HSLToRGB(removeDeg(h) / 360, removePercent(s) / 100, removePercent(l) / 100);
}

/**
 * Converts RGB color values to HSL.
 * 
 * @param r - The red component, a number between 0 and 255.
 * @param g - The green component, a number between 0 and 255.
 * @param b - The blue component, a number between 0 and 255.
 * @returns An object with the HSL representation, with each component (h, s, l) as a number between 0 and 1.
 * 
 * @example
 * ```typescript
 * const hsl = RGBToHSL(255, 0, 0);
 * console.log(hsl); // { h: 0, s: 1, l: 0.5 }
 * ```
 */
export function RGBToHSL(r: number, g: number, b: number): { h: number, s: number, l: number } {
    r /= 255;
    g /= 255;
    b /= 255;

    const max = Math.max(r, g, b),
        min = Math.min(r, g, b);

    let h = 0,
        s = 0,
        l = (max + min) / 2;

    if (max === min) {
        h = s = 0; // achromatic
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch (max) {
            case r:
                h = (g - b) / d + (g < b ? 6 : 0);
                break;
            case g:
                h = (b - r) / d + 2;
                break;
            case b:
                h = (r - g) / d + 4;
                break;
        }
        h /= 6;
    }

    return { h: h, s: s, l: l };
}

/**
 * Converts an HSL color value to RGB.
 * 
 * @param h - The hue, a number between 0 and 1.
 * @param s - The saturation, a number between 0 and 1.
 * @param l - The lightness, a number between 0 and 1.
 * @returns An object with the RGB representation, with each component (r, g, b) as a number between 0 and 255.
 * 
 * @example
 * ```typescript
 * const rgb = HSLToRGB(0.5, 0.5, 0.5);
 * console.log(rgb); // { r: 64, g: 191, b: 191 }
 * ```
 */
export function HSLToRGB(h: number, s: number, l: number): { r: number, g: number, b: number } {
    let r: number, g: number, b: number;

    if (s === 0) {
        r = g = b = l; // achromatic
    } else {
        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;
        const hue2rgb = (p: number, q: number, t: number) => {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1 / 6) return p + (q - p) * 6 * t;
            if (t < 1 / 2) return q;
            if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
            return p;
        };
        r = hue2rgb(p, q, h + 1 / 3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1 / 3);
    }

    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
    };
}