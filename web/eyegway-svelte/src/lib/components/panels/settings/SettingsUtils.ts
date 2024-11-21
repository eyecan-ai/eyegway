import { ConfigurationUtils } from '../../utils/ConfigurationUtils.js';
import { StyleSettings } from './SettingsModel.js';

const defaultStyleSettings = new StyleSettings();

export class StyleSettingsUtils extends ConfigurationUtils<StyleSettings> {
    constructor() {
        super('StyleSettings', defaultStyleSettings);
    }
}