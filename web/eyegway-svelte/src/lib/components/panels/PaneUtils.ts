import { ConfigurationUtils } from '../utils/ConfigurationUtils.js';
import { PaneConfiguration } from './PaneModel.js';

export class PaneConfigurationUtils extends ConfigurationUtils<PaneConfiguration> {
    constructor() {
        super(
            'EyegwayPaneConfiguration',
            PaneConfiguration,
            import.meta.glob("/public/layouts/*.json", { eager: true }),
            '/public/layouts/default_layout.json'
        );
    }
}