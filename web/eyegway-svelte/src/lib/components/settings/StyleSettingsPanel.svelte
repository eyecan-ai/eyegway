<script lang="ts">
	import { Button, Color, Folder, Pane, Slider, ThemeUtils, Point } from 'svelte-tweakpane-ui';
	import { styleSettings, styleSettingsReset } from './StyleSettingsStore.js';
</script>

<Pane position={'inline'} theme={ThemeUtils.presets.light} width={350}>
	<Folder title="Point Clouds">
		<Color bind:value={$styleSettings.pcd.background} label="Background Color" />

		<Slider
			bind:value={$styleSettings.pcd.point_size}
			min={0.0001}
			max={0.1}
			format={(v) => v.toFixed(4)}
			label="Point Size"
		/>
		<Slider
			bind:value={$styleSettings.pcd.distance}
			min={0.1}
			max={2.0}
			format={(v) => v.toFixed(4)}
			label="Camera Distance"
		/>
		<Color bind:value={$styleSettings.pcd.grid_color} label="Grid Color" />
		<Slider
			bind:value={$styleSettings.pcd.grid_size}
			min={0.01}
			max={5.0}
			format={(v) => v.toFixed(4)}
			label="Grid Size [m]"
		/>
		<Slider
			bind:value={$styleSettings.pcd.grid_tile}
			min={0.01}
			max={5.0}
			format={(v) => v.toFixed(4)}
			label="Grid Tile Size [m]"
		/>
	</Folder>

	<Folder title="">
		<Button on:click={styleSettingsReset} title="Reset Defaults" />
	</Folder>
</Pane>
