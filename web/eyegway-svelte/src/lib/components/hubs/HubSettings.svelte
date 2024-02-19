<script lang="ts">
	import { Parameters } from '$lib/Parameters.js';
	import { ServerPreferences } from '$lib/Stores.js';
	import { Button, Text, Slider } from 'svelte-tweakpane-ui';

	export let host: string = $ServerPreferences.host;

	$: $ServerPreferences.host = host;
</script>

<div>
	<Text bind:value={host} label="Host" />
</div>
