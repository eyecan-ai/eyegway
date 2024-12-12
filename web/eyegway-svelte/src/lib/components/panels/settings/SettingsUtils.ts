import { ConfigurationUtils } from '../../utils/ConfigurationUtils.js';
import { type StyleSettings, StyleSettingsSchema } from './SettingsModel.js';

export class StyleSettingsUtils extends ConfigurationUtils<StyleSettings> {
    constructor() {
        super(
            'EyegwayStyleSettings',
            StyleSettingsSchema,
            import.meta.glob("/public/themes/*.json", { eager: true }),
            '/public/themes/default.json'
        );
    }
}