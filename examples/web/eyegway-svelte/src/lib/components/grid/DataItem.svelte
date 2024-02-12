<script lang="ts">
	import { GridItem } from 'svelte-grid-extended';
	import { DataImage, DataMetadata, DataPointCloud, DataTensor, ProtoypeItem } from './Data.js';
	import PointCloudView from '../views/PointCloud/PointCloudView.svelte';
	import MetadataView from '../views/MetadataView.svelte';
	import MatrixView from '../views/MatrixView.svelte';

	export let prototype: ProtoypeItem | null = null;
	export let data: any = null;
	let value: any | null = null;

	function getValueByDotNotation(obj: any, dotNotation: string) {
		const keys = dotNotation.split('.');
		let value = obj;
		console.log('GEeting ', obj, dotNotation, keys);

		for (const key of keys) {
			if (key in value) {
				console.log('Sub', key, value, value[key]);
				value = value[key];
			} else {
				return undefined;
			}
		}

		return value;
	}

	$: {
		if (prototype && data) {
			value = getValueByDotNotation(data, prototype.name);
			console.log('Valued', data, prototype.name);
		}
	}
</script>

{#if prototype}
	<GridItem x={prototype.x} y={prototype.y} w={prototype.w} h={prototype.h} class="item">
		<div class="item">
			{#if value}
				{#if value instanceof DataImage}
					<img class="item-image" src={value.url} alt="thumbnail" draggable="false" />
				{:else if value instanceof DataPointCloud}
					<PointCloudView
						pointcloud={{
							vertices: value.vertices,
							colors: value.colors
						}}
					/>
				{:else if value instanceof DataTensor}
					<MatrixView tensor={value.tensor} />
				{:else if value instanceof DataMetadata}
					<MetadataView metadata={value.data} />
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
		/* place-items: stretch; */
		background-color: #222;
		width: 100%;
		height: 100%;
		overflow: scroll;
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
