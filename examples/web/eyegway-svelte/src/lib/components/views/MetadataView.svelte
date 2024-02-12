<script lang="ts">
	import { JSONEditor } from 'svelte-jsoneditor';

	export let filter: string | null = null;
	export let metadata: any = {};
	let filteredMetadata: any = {};
	let filteringError: boolean = false;

	$: {
		if (metadata) {
			// Check if metadata contains filter
			// If not, set metadata to empty object
			filteringError = false;
			if (filter !== null && metadata[filter] === undefined) {
				filteredMetadata = {};
				filteringError = true;
			} else {
				filteredMetadata = metadata[filter];
			}
		}
	}
</script>

<div>
	{#if filteringError}
		<div class="notification is-danger">
			Filter Key "<b>{filter}</b>" not found
		</div>
	{:else}
		<JSONEditor
			content={{ json: metadata }}
			mainMenuBar={false}
			navigationBar={false}
			statusBar={false}
			readOnly
		/>
	{/if}
</div>
