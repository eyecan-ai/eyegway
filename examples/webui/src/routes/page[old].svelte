<script lang="ts">
	import DynamicItem from '$lib/components/DynamicItem.svelte';
	import DynamicItemProtoype from '$lib/components/ItemPlaceholder.svelte';
	import PointCloudViewer from '$lib/components/PointCloudViewer.svelte';
	import { CustomConnector, EImage, EPointCloud } from '$lib/eyegway/CustomConnector';
	import { EyegwayClient } from '$lib/eyegway/EyegwayClient';
	import { onMount } from 'svelte';
	import Grid, { GridItem } from 'svelte-grid-extended';

	console.log('ciao');

	let sample: any = {};
	let ready: boolean = false;

	onMount(async () => {
		const hubName = 'fai4ba';
		const client = EyegwayClient.getInstance();
		client.setConnector(new CustomConnector());
		sample = await client.last(hubName, 0);
		console.log(sample);
		ready = true;
	});
</script>

<div class="container">
	{#if ready}
		<Grid cols={8} rows={8}>
			<DynamicItemProtoype x={0} y={0} w={3} h={3} name={'gino'} />
			<DynamicItemProtoype x={3} y={0} w={3} h={3} name={'pino'} />
			<!-- <GridItem x={0} y={0} w={3} h={3} class="item">
				<div class="gino">
					<img class="item-image" src={sample['front_left_image'].url} alt="thumbnail" />
				</div>
			</GridItem> -->
			<!-- <GridItem x={3} y={3} w={4} class="item">Hoy</GridItem> -->
		</Grid>
	{/if}
</div>

<!-- <div class="columns is-multiline">
	{#each Object.keys(sample) as key}
		<div class="column is-4">
			<div class="card">
				<header class="card-header">
					<p class="card-header-title">{key}</p>
				</header>
				<div class="card-image">
					{#if sample[key] instanceof EImage}
						<img src={sample[key].url} alt="thumbnail" />
					{:else if sample[key] instanceof EPointCloud}
						<div>
							<PointCloudViewer pointcloud={sample[key]} width={300} height={300} />
						</div>
					{:else}
						<button>Meta</button>
					{/if}
				</div>
			</div>
		</div>
	{/each}
</div> -->

<style>
	.card-image {
		width: 100%;
		height: 300px;
		background-color: red;
	}
	.card-image img,
	.card-image > div {
		width: 100%;
		height: 300px;
		object-fit: contain;
	}
	.item-image {
		background-color: black;
		height: 100%;
		width: 100%;
		object-fit: contain;
		position: absolute;
	}
	.gino {
		position: relative;
		background-color: blue;
		padding: 0px;
		position: absolute;
		width: 100%;
		height: 100%;
		position: relative;
	}
	.container {
		background-color: green;
		height: 500px;
		margin-top: 64px;
	}
	:global(.item) {
		display: grid;
		place-items: center;
		background-color: red;
		width: 100%;
		height: 100%;
		font-size: xx-large;
	}
	:global(.item):hover .item-image {
		display: none;
	}
</style>
