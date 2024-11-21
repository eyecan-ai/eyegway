<script lang="ts">
	import { JSONEditor, Mode } from 'svelte-jsoneditor';
	import type { DataMetadata } from '../PaneModel.js';
	import type { MetadataSettings } from '../settings/SettingsModel.js';

	export let userData: DataMetadata | null = null;
	export let userSettings: MetadataSettings | null = null;
</script>

{#if userData && userSettings}
	<JSONEditor
		content={{ json: userData.data }}
		mode={Mode[userSettings.mode]}
		mainMenuBar={false}
		navigationBar={false}
		statusBar={false}
		readOnly
	/>
{/if}
