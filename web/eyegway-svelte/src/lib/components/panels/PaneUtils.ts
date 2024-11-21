import { ConfigurationUtils } from '../utils/ConfigurationUtils.js';
import { PaneConfiguration } from './PaneModel.js';

const defaultPaneConfiguration = new PaneConfiguration();

export class PaneConfigurationUtils extends ConfigurationUtils<PaneConfiguration> {
    constructor() {
        super('PaneConfiguration', PaneConfiguration);
    }
}