<script lang="ts">
	import { JSONEditor } from 'svelte-jsoneditor';
	import type { DataMetadata } from '../MosaicModel.js';

	export let userData: DataMetadata | null = null;
</script>

{#if userData}
	<JSONEditor
		content={{ json: userData.data }}
		mainMenuBar={false}
		navigationBar={false}
		statusBar={false}
		readOnly
	/>
{/if}
