<script lang="ts">
	import {
		Button,
		Color,
		Folder,
		Pane,
		Slider,
		ThemeUtils,
		Point,
		List,
		type ListOptions
	} from 'svelte-tweakpane-ui';
	import { ImageSettings } from './SettingsModel.js';

	export let userSettings: ImageSettings | null = null;

	const options: ListOptions<string> = {
		contain: 'contain',
		cover: 'cover'
	};
	let selection: number = 1;
</script>

{#if userSettings}
	<Pane position={'inline'} theme={ThemeUtils.presets.jetblack}>
		<Folder title="Image Viewer Settings"></Folder>
		<List bind:value={userSettings.fit} {options} label="Fit" />

		<Button on:click={() => (userSettings = new ImageSettings())} title="Reset Defaults" />
	</Pane>
{/if}
