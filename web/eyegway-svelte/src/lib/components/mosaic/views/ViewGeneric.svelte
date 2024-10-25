<script lang="ts">
	import {
		DataImage,
		DataMetadata,
		DataPointCloud,
		DataTensor,
		DataPlot,
		type GenericData
	} from '../MosaicModel.js';
	import ViewImage from './ViewImage.svelte';
	import ViewMatrix from './ViewMatrix.svelte';
	import ViewMetadata from './ViewMetadata.svelte';
	import ViewPointCloud from './ViewPointCloud.svelte';
	import ViewPlot from './ViewPlot.svelte';

	export let userData: GenericData | null = null;
</script>

{#if userData instanceof DataImage}
	<ViewImage {userData} />
{:else if userData instanceof DataTensor}
	<ViewMatrix {userData} />
{:else if userData instanceof DataMetadata}
	<ViewMetadata {userData} />
{:else if userData instanceof DataPointCloud}
	<ViewPointCloud {userData} />
{:else if userData instanceof DataPlot}
	<ViewPlot {userData} />
{/if}
