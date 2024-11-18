import { type Writable } from 'svelte/store';
import { persisted } from 'svelte-persisted-store';

export interface ColorStyle {
	logo: string;
	panel: string;
	panel_unselected: string;
	header: string;
	container: string;
	background: string;
	internal_gradient: string;
	external_gradient: string;
	header_buttons: string;
}

export class StyleSettings {
	// Global
	color: ColorStyle = {
		logo: 'images/logo.png',
		panel: '#fff',
		panel_unselected: '#fdfdfd6c',
		header: '#ffffff',
		container: '#ffffff',
		background: '#ffffff',
		internal_gradient: '#ffffff',
		external_gradient: '#ebebeb',
		header_buttons: '#444444'
	};
}

export const styleSettings: Writable<StyleSettings> = persisted(
	'StyleSettingsPanels',
	new StyleSettings()
);

export const styleSettingsReset = () => {
	styleSettings.set(new StyleSettings());
};
