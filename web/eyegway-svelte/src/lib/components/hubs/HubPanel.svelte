<script lang="ts">
	import { HubsPreferences } from '$lib/Stores.js';
	import HubPlayer from './HubPlayer.svelte';
	import HubSelector from './HubSelector.svelte';
	import { EllipsisVertical } from 'lucide-svelte';

	export let data: any | null = null;
	export let hubName: string | null = $HubsPreferences.activeHub;
</script>

<div class="columns is-justify-content-flex-end is-vcentered is-variable is-0">
	<div class="column is-narrow">
		<HubPlayer bind:data {hubName} />
	</div>
	<div class="column is-narrow is-flex">
		<EllipsisVertical strokeWidth={0.5} />
	</div>
	<div class="column is-narrow">
		<HubSelector bind:hubName />
	</div>
</div>
