<script lang="ts">
	import { EyegwayHubClient, EyegwayTensor } from '$lib/Eyegway.js';

	import Composer from '$lib/components/grid/Composer.svelte';
	import { onMount } from 'svelte';

	let hubName: string = 'fai4ba';
	let historySize: number = -1;
	let bufferSize: number = -1;
	let matrix: EyegwayTensor | null = null;
	let metadata: any = {};
	let sharedData: any = {};

	async function update() {
		const client = new EyegwayHubClient(hubName);
		historySize = await client.historySize();
		bufferSize = await client.bufferSize();

		let offset = Math.floor(Math.random() * (historySize - 1));
		sharedData = await client.last(offset);
		console.log(sharedData);
	}
	onMount(async () => {
		await update();
	});
</script>

<div>
	<input class="input" bind:value={hubName} />
	<button class="button" on:click={update}>Update</button>
</div>
<div>
	<div>History Size: {historySize}</div>
	<div>Buffer Size: {bufferSize}</div>
</div>

<div class="box">
	<Composer {sharedData} />
</div>
