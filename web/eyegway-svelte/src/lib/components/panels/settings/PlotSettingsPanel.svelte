<script lang="ts">
	import { Checkbox, Separator, Button, Pane, Slider, ThemeUtils } from 'svelte-tweakpane-ui';
	import { PlotSettings } from './SettingsModel.js';

	export let userSettings: PlotSettings | null;
</script>

{#if userSettings}
	<Pane position={'inline'} title="Plot Viewer Settings" theme={ThemeUtils.presets.jetblack}>
		<Checkbox bind:value={userSettings.fillParent} label="Fill Parent" />
		<Slider bind:value={userSettings.debounce} label="Debounce" min={0} max={200} step={10} />
		<Separator />
		<Button on:click={() => (userSettings = new PlotSettings())} title="Reset Defaults" />
	</Pane>
{/if}
