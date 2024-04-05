import { type Writable } from 'svelte/store';
import { persisted } from 'svelte-persisted-store';

export interface PCDStyle {
	background: string;
	grid_color: string;
	grid_tile: number;
	grid_size: number;
	point_size: number;
	distance: number;
}

export class StyleSettings {
	pcd: PCDStyle = {
		background: '#222',
		grid_color: '#888',
		grid_tile: 0.1,
		grid_size: 1,
		point_size: 0.01,
		distance: 1.0
	};
}

export let styleSettings: Writable<StyleSettings> = persisted('StyleSettings', new StyleSettings());

export let styleSettingsReset = () => {
	styleSettings.set(new StyleSettings());
};
