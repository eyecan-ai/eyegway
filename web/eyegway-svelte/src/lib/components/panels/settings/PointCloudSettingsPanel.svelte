<script lang="ts">
	import { Button, Color, Separator, Pane, Slider, ThemeUtils } from 'svelte-tweakpane-ui';
	import { PointCloudSettings } from './SettingsModel.js';

	export let userSettings: PointCloudSettings | null;
</script>

{#if userSettings}
	<Pane position={'inline'} title="Point Clouds Viewer Settings">
		<Color bind:value={userSettings.background} label="Background Color" />

		<Slider
			bind:value={userSettings.pointSize}
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
		<Color bind:value={userSettings.gridColor} label="Grid Color" />
		<Slider
			bind:value={userSettings.gridSize}
			min={0.01}
			max={5.0}
			format={(v) => v.toFixed(4)}
			label="Grid Size [m]"
		/>
		<Slider
			bind:value={userSettings.gridTile}
			min={0.01}
			max={5.0}
			format={(v) => v.toFixed(4)}
			label="Grid Tile Size [m]"
		/>
		<Separator />
		<Button on:click={() => (userSettings = new PointCloudSettings())} title="Reset Defaults" />
	</Pane>
{/if}
