<script lang="ts">
	import { EyegwayHubClient } from 'eyegway-svelte';
	import { Mosaic, HubConnector } from 'eyegway-svelte';

	let data: any = null;
	let editableMosaic: boolean = true;

	async function test() {
		const client = new EyegwayHubClient('fai4ba');
		data = await client.last(10);
		console.log(data);
	}
</script>

<div>
	<button on:click={test}>Test</button>
	<HubConnector bind:data />
	<Mosaic {data} editableMode={editableMosaic} />
</div>
