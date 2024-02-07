<script lang="ts">
	import { EyegwayHubClient, EyegwayImage, EyegwayTensor } from '$lib/Eyegway.js';
	import Metadata from '$lib/components/metadata/Metadata.svelte';
	import MetadataCustom from '$lib/components/metadata/MetadataCustom.svelte';
	import TensorTable from '$lib/components/tensors/TensorTable.svelte';

	import { encode } from '@msgpack/msgpack';

	let hubName: string = 'fai4ba';
	let historySize: number = -1;
	let bufferSize: number = -1;
	let matrix: EyegwayTensor | null = null;
	let metadata: any = {};

	async function update() {
		const client = new EyegwayHubClient(hubName);
		historySize = await client.historySize();
		bufferSize = await client.bufferSize();

		let offset = parseInt(Math.random() * (historySize - 1));
		let data = await client.last(offset);

		matrix = data.front_right_world2cam;
		metadata = data.marker_cfg;
		console.log(data);

		// let data = (await client.last()).front_left_image as EyegwayImage;
		// data = await data.convertToEyegwayImageUint8();
		// // data = await data.convertoToEyegwayImageBlob();
		// console.log(data);
		// const buff = await (await fetch(data.data)).arrayBuffer();
		// console.log(new Uint8Array(buff));
		// data = await data.convertToEyegwayImageUint8();

		// console.log(data);

		// const client2 = new EyegwayHubClient('commands');
		// await client2.clear();
		// console.log(await client2.historySize(), await client2.bufferSize());

		// console.log('Pushing', await client2.push({ image: data }));
		// const lastData: { image: EyegwayImage } = await client2.last();
		// console.log(lastData);
		// const image = new Image();
		// image.src = data.imageUrl();
		// image.width = 128;

		// document.body.appendChild(image);
	}
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
	<TensorTable tensor={matrix} />

	<MetadataCustom {metadata} />
</div>
