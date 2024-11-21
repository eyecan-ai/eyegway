<script lang="ts">
	import { Button, Separator, Pane, Slider, ThemeUtils } from 'svelte-tweakpane-ui';
	import { MatrixSettings } from './SettingsModel.js';

	export let userSettings: MatrixSettings | null;
</script>

{#if userSettings}
	<Pane position={'inline'} title="Matrix Viewer Settings" theme={ThemeUtils.presets.jetblack}>
		<Slider
			bind:value={userSettings.numFractionDigits}
			label="Number of Fraction Digits"
			min={0}
			max={10}
			step={1}
		/>
		<Slider bind:value={userSettings.maxElements} label="Max Elements" min={1} max={256} step={1} />
		<Separator />
		<Button on:click={() => (userSettings = new MatrixSettings())} title="Reset Defaults" />
	</Pane>
{/if}
