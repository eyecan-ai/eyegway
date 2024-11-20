<script lang="ts">
	import { Button, Color, Folder, Pane, Slider, ThemeUtils, Point } from 'svelte-tweakpane-ui';
	import { MatrixSettings } from './SettingsModel.js';

	export let userSettings: MatrixSettings | null;
</script>

{#if userSettings}
	<Pane position={'inline'} theme={ThemeUtils.presets.jetblack}>
		<Folder title="Matrix Viewer Settings"></Folder>

		<Button on:click={() => (userSettings = new MatrixSettings())} title="Reset Defaults" />
	</Pane>
{/if}
