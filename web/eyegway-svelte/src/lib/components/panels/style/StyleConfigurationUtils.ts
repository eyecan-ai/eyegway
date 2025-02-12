import { ConfigurationUtils } from '../../utils/ConfigurationUtils.js';
import { type StyleConfiguration, StyleSettingsSchema } from './StyleModel.js';
import { Parameters } from '$lib/Parameters.js';

export class StyleConfigurationUtils extends ConfigurationUtils<StyleConfiguration> {
    constructor() {
        super(
            'EyegwayStyleSettings',
            StyleSettingsSchema,
            Parameters.themes.split(/;|:/).map(theme => `/themes/${theme.trim()}.json`),
            `/themes/${Parameters.defaultTheme}.json`
        );
    }
}