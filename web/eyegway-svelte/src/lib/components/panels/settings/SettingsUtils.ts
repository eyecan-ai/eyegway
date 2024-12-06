import { ConfigurationUtils } from '../../utils/ConfigurationUtils.js';
import { StyleSettings } from './SettingsModel.js';

export class StyleSettingsUtils extends ConfigurationUtils<StyleSettings> {
    constructor() {
        super(
            'EyegwayStyleSettings',
            StyleSettings,
            import.meta.glob("/public/themes/*.json", { eager: true }),
            '/public/themes/default.json'
        );
    }
}