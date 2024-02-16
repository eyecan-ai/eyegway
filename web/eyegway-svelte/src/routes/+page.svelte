<script lang="ts">
	import HubConnector from '$lib/components/hubs/HubConnector.svelte';
	import Mosaic from '$lib/components/mosaic/Mosaic.svelte';

	let sharedData: any | null = null;
	let editableMosaic: boolean = false;
	let mosaic: Mosaic;
</script>

<div class="box container mb-1 mt-2">
	<HubConnector bind:data={sharedData} />
</div>

<div class="box container p-0 mt-0">
	<Mosaic bind:this={mosaic} data={sharedData} editableMode={editableMosaic} />
</div>
