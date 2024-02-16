<script lang="ts">
	import HubPlayer from './HubPlayer.svelte';
	import HubSelector from './HubSelector.svelte';
	import { IconDotsVertical } from '@tabler/icons-svelte';

	export let data: any | null = null;
	export let hubName: string | null = null;
</script>

<div class="columns is-justify-content-flex-end is-vcentered is-variable is-0">
	<div class="column is-narrow">
		<HubPlayer bind:data {hubName} />
	</div>
	<div class="column is-narrow">
		<IconDotsVertical stroke={1} />
	</div>
	<div class="column is-narrow">
		<HubSelector bind:hubName />
	</div>
</div>
