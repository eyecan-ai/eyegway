<script lang="ts">
	import { ServerPreferences } from '$lib/Stores.js';
	import { Text } from 'svelte-tweakpane-ui';

	export let host: string = $ServerPreferences.host;

	$: $ServerPreferences.host = host;
</script>

<div>
	<Text bind:value={host} label="Host" />
</div>
