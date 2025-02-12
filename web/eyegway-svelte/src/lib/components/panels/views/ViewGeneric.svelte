<script lang="ts">
	import {
		DataImage,
		DataMetadata,
		DataPointCloud,
		DataTensor,
		DataPlot,
		type GenericData
	} from '../PaneModel.js';
	import ViewImage from './ViewImage.svelte';
	import ViewMatrix from './ViewMatrix.svelte';
	import ViewMetadata from './ViewMetadata.svelte';
	import ViewPointCloud from './ViewPointCloud.svelte';
	import ViewPlot from './ViewPlot.svelte';
	import {
		ImageSettings,
		MetadataSettings,
		PointCloudSettings,
		MatrixSettings,
		PlotSettings,
		type GenericSettings
	} from '../settings/SettingsModel.js';

	export let userData: GenericData | null = null;
	export let userSettings: GenericSettings | null = null;
</script>

{#if userData instanceof DataImage && userSettings instanceof ImageSettings}
	<ViewImage {userData} {userSettings} />
{:else if userData instanceof DataTensor && userSettings instanceof MatrixSettings}
	<ViewMatrix {userData} {userSettings} />
{:else if userData instanceof DataMetadata && userSettings instanceof MetadataSettings}
	<ViewMetadata {userData} {userSettings} />
{:else if userData instanceof DataPointCloud && userSettings instanceof PointCloudSettings}
	<ViewPointCloud {userData} {userSettings} />
{:else if userData instanceof DataPlot && userSettings instanceof PlotSettings}
	<ViewPlot {userData} {userSettings} />
{/if}
