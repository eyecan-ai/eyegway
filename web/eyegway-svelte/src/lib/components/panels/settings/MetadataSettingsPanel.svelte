<script lang="ts">
	import { Button, List, type ListOptions, Pane, ThemeUtils, Separator } from 'svelte-tweakpane-ui';
	import { MetadataSettings } from './SettingsModel.js';

	export let userSettings: MetadataSettings | null;

	const options: ListOptions<string> = {
		text: 'text',
		tree: 'tree',
		table: 'table'
	};
</script>

{#if userSettings}
	<Pane position={'inline'} title="Metadata Viewer Settings" theme={ThemeUtils.presets.jetblack}>
		<List bind:value={userSettings.mode} {options} label="Mode" />
		<Separator />
		<Button on:click={() => (userSettings = new MetadataSettings())} title="Reset Defaults" />
	</Pane>
{/if}
