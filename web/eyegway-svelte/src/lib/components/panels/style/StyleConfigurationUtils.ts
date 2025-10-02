import { ConfigurationUtils } from '../../utils/ConfigurationUtils.js';
import { type StyleConfiguration, StyleSettingsSchema } from './StyleModel.js';
import { Parameters } from '$lib/Parameters.js';
import { resolve } from '$app/paths';

export class StyleConfigurationUtils extends ConfigurationUtils<StyleConfiguration> {
	constructor() {
		super(
			'EyegwayStyleSettings',
			StyleSettingsSchema,
			Parameters.themes.split(/;|:/).map((theme) => resolve(`/themes/${theme.trim()}.json`)),
			resolve(`/themes/${Parameters.defaultTheme.trim()}.json`)
		);
	}
}
