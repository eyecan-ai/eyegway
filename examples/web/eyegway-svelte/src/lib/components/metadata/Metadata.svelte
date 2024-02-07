<script lang="ts">
	import { JSONEditor } from 'svelte-jsoneditor';

	export let metadata: any = {};
	let content = { json: metadata };

	$: if (metadata) {
		content = {
			json: metadata
		};
	}
</script>

<div>
	<JSONEditor {content} mode={'tree'} readOnly mainMenuBar={false} navigationBar={false} />
</div>
