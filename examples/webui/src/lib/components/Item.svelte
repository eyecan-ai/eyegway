<script lang="ts">
	import { GridItem } from 'svelte-grid-extended';
	import type { ProtoypeItem } from './items/DynamicGrid';
	import { EImage, EPointCloud, type ETensor } from '$lib/eyegway/CustomConnector';
	import PointCloudViewer from './PointCloudViewer.svelte';

	export let prototype: ProtoypeItem | null = null;
	export let data: any = null;
	let value: EImage | ETensor | EPointCloud | null = null;

	$: {
		if (prototype) {
			value = data[prototype.name];
		}
	}
</script>

{#if prototype}
	<GridItem x={prototype.x} y={prototype.y} w={prototype.w} h={prototype.h} class="item">
		<div class="item">
			{#if value}
				{#if value instanceof EImage}
					<img class="item-image" src={value.url} alt="thumbnail" draggable="false" />
				{:else if value instanceof EPointCloud}
					<PointCloudViewer pointcloud={value} width={300} height={300} />
				{/if}
			{/if}
			<div class="banner">
				{prototype.name}
			</div>
		</div>
	</GridItem>
{/if}

<style>
	.item {
		display: grid;
		place-items: center;
		background-color: #222;
		width: 100%;
		height: 100%;
		overflow: hidden;
		box-shadow: 0px 0px 5px 0px #222;
	}
	.item img {
		width: 100%;
		height: 100%;
		object-fit: contain;
	}
	.item .banner {
		position: absolute;
		bottom: 0;
		left: 0;
		color: #222;
		background-color: #fafafa;

		padding: 3px;
		border-radius: 5px 5px 0px 0px;
		opacity: 0.3;
		width: 100%;
		font-size: 0.8em;
		transition: all 0.3s;
	}
	.item:hover .banner {
		opacity: 1;
	}
</style>
