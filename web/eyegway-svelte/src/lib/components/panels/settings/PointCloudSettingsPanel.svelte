<script lang="ts">
	import { Button, Color, Folder, Pane, Slider, ThemeUtils, Point } from 'svelte-tweakpane-ui';
	import { PointCloudSettings } from './SettingsModel.js';

	export let userSettings: PointCloudSettings | null;
</script>

{#if userSettings}
	<Pane position={'inline'} theme={ThemeUtils.presets.jetblack}>
		<Folder title="Point Clouds Viewer Settings">
			<Color bind:value={userSettings.background} label="Background Color" />

			<Slider
				bind:value={userSettings.point_size}
				min={0.0001}
				max={0.1}
				format={(v) => v.toFixed(4)}
				label="Point Size"
			/>
			<Slider
				bind:value={userSettings.distance}
				min={0.1}
				max={2.0}
				format={(v) => v.toFixed(4)}
				label="Camera Distance"
			/>
			<Color bind:value={userSettings.grid_color} label="Grid Color" />
			<Slider
				bind:value={userSettings.grid_size}
				min={0.01}
				max={5.0}
				format={(v) => v.toFixed(4)}
				label="Grid Size [m]"
			/>
			<Slider
				bind:value={userSettings.grid_tile}
				min={0.01}
				max={5.0}
				format={(v) => v.toFixed(4)}
				label="Grid Tile Size [m]"
			/>
		</Folder>

		<Button on:click={() => (userSettings = new PointCloudSettings())} title="Reset Defaults" />
	</Pane>
{/if}
