<script lang="ts">
	import { Button, Separator, Pane, ThemeUtils, List, type ListOptions } from 'svelte-tweakpane-ui';
	import { ImageSettings } from './SettingsModel.js';

	export let userSettings: ImageSettings | null = null;

	const options: ListOptions<string> = {
		contain: 'contain',
		cover: 'cover'
	};
</script>

{#if userSettings}
	<Pane position={'inline'} title="Image Viewer Settings">
		<List bind:value={userSettings.fit} {options} label="Fit" />
		<Separator />
		<Button on:click={() => (userSettings = new ImageSettings())} title="Reset Defaults" />
	</Pane>
{/if}
