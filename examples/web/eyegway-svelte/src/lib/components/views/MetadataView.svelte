<script lang="ts">
	import { JSONEditor } from 'svelte-jsoneditor';

	export let metadata: any = {};
</script>

<div>
	<JSONEditor
		content={{ json: metadata }}
		mainMenuBar={false}
		navigationBar={false}
		statusBar={false}
		readOnly
	/>
</div>
