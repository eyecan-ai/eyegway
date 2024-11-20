<script lang="ts">
	import { Button, Color, Folder, Pane, Slider, ThemeUtils, Point } from 'svelte-tweakpane-ui';
	import { PlotSettings } from './SettingsModel.js';

	export let userSettings: PlotSettings | null;
</script>

{#if userSettings}
	<Pane position={'inline'} theme={ThemeUtils.presets.jetblack}>
		<Folder title="Plot Viewer Settings"></Folder>

		<Button on:click={() => (userSettings = new PlotSettings())} title="Reset Defaults" />
	</Pane>
{/if}
