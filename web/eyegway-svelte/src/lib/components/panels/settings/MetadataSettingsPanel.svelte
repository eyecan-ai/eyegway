<script lang="ts">
	import { Button, Color, Folder, Pane, Slider, ThemeUtils, Point } from 'svelte-tweakpane-ui';
	import { MetadataSettings } from './SettingsModel.js';

	export let userSettings: MetadataSettings | null;
</script>

{#if userSettings}
	<Pane position={'inline'} theme={ThemeUtils.presets.jetblack}>
		<Folder title="Metadata Viewer Settings"></Folder>

		<Button on:click={() => (userSettings = new MetadataSettings())} title="Reset Defaults" />
	</Pane>
{/if}
