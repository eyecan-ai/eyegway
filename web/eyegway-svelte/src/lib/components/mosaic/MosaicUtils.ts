import { browser } from '$app/environment';
import type { MosaicConfiguration } from './MosaicModel.js';

export class MosaicConfigurationsUtils {
	static DEFAULT_CONFIGURATION_NAME = 'Default';

	/**
	 * Save the configuration to a file
	 * @param configuration the configuration to save
	 * @returns
	 */
	static saveConfigurationToFile(configuration: MosaicConfiguration): void {
		if (browser) {
			const currentDate = new Date();
			const configurationName = prompt('Please enter configuration name', currentDate.toJSON());
			if (configurationName == null) {
				return;
			}
			const blob = new Blob([JSON.stringify(configuration)], { type: 'application/json' });
			const url = URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = configurationName + '.json';
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
			URL.revokeObjectURL(url);
		}
	}

	/**
	 * Load the configuration from a file. Returns a promise that resolves to the configuration
	 * @returns
	 */
	static loadConfigurationFromFile(): Promise<MosaicConfiguration> {
		return new Promise((resolve, reject) => {
			if (browser) {
				const input = document.createElement('input');
				input.type = 'file';
				input.accept = '.json';
				input.onchange = (event) => {
					const file = (event.target as HTMLInputElement).files?.[0];
					if (file) {
						const reader = new FileReader();
						reader.onload = (event) => {
							try {
								const configuration = JSON.parse(
									event.target?.result as string
								) as MosaicConfiguration;
								resolve(configuration);
							} catch (error) {
								reject(error);
							}
						};
						reader.readAsText(file);
					}
				};
				input.click();
			}
		});
	}

	static saveConfigurationAsDefault(configuration: MosaicConfiguration): void {
		if (browser)
			localStorage.setItem(
				MosaicConfigurationsUtils.DEFAULT_CONFIGURATION_NAME,
				JSON.stringify(configuration)
			);
	}

	static loadDefaultConfiguration(): MosaicConfiguration | null {
		if (browser) {
			const configuration = localStorage.getItem(
				MosaicConfigurationsUtils.DEFAULT_CONFIGURATION_NAME
			);
			if (configuration) {
				return JSON.parse(configuration) as MosaicConfiguration;
			}
		}
		return null;
	}
}
