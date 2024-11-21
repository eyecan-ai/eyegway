import { ConfigurationUtils } from '../utils/ConfigurationUtils.js';
import { PaneConfiguration } from './PaneModel.js';

export class PaneConfigurationUtils extends ConfigurationUtils<PaneConfiguration> {
    constructor() {
        super('EyegwayPaneConfiguration', PaneConfiguration);
    }
}