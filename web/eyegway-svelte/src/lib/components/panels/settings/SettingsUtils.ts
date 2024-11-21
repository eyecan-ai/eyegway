import { ConfigurationUtils } from '../../utils/ConfigurationUtils.js';
import { StyleSettings } from './SettingsModel.js';

export class StyleSettingsUtils extends ConfigurationUtils<StyleSettings> {
    constructor() {
        super('EyegwayStyleSettings', StyleSettings);
    }
}