import { ConfigurationUtils } from '../utils/ConfigurationUtils.js';
import { type PaneConfiguration, PaneConfigurationSchema } from './PaneModel.js';

export class PaneConfigurationUtils extends ConfigurationUtils<PaneConfiguration> {
    constructor() {
        super(
            'EyegwayPaneConfiguration',
            PaneConfigurationSchema,
            import.meta.glob("/public/layouts/*.json", { eager: true }),
            '/public/layouts/default.json'
        );
    }
}