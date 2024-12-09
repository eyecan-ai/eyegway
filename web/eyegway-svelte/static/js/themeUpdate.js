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
window.updateCSSVariables = function (styles, prefix = '') {
    if (typeof document === 'undefined') return;

    for (const [key, value] of Object.entries(styles)) {
        if (typeof value === 'object' && value !== null) {
            window.updateCSSVariables(value, `${prefix}${key}-`);
        } else {
            const cssVarName = `--${prefix}${key.replace(/_/g, '-')}`;
            document.documentElement.style.setProperty(cssVarName, value);
        }
    }
};