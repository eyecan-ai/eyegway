import { ConfigurationUtils } from '../utils/ConfigurationUtils.js';
import { type PaneConfiguration, PaneConfigurationSchema } from './PaneModel.js';
import { Parameters } from '$lib/Parameters.js';
import { resolve } from '$app/paths';

export class PaneConfigurationUtils extends ConfigurationUtils<PaneConfiguration> {
	constructor() {
		super(
			'EyegwayPaneConfiguration',
			PaneConfigurationSchema,
			Parameters.layouts.split(/;|:/).map((layout) => resolve(`/layouts/${layout.trim()}.json`)),
			resolve(`/layouts/${Parameters.defaultLayout.trim()}.json`)
		);
	}
}
