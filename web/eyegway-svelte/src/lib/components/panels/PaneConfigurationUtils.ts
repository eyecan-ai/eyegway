import { ConfigurationUtils } from '../utils/ConfigurationUtils.js';
import { type PaneConfiguration, PaneConfigurationSchema } from './PaneModel.js';
import { Parameters } from '$lib/Parameters.js';

export class PaneConfigurationUtils extends ConfigurationUtils<PaneConfiguration> {
    constructor() {
        super(
            "EyegwayPaneConfiguration",
            PaneConfigurationSchema,
            Parameters.layouts.split(/;|:/).map(layout => `/layouts/${layout.trim()}.json`),
            `/layouts/${Parameters.defaultLayout.trim()}.json`
        );
    }
}