<script lang="ts">
	import {
		ImageSettings,
		MetadataSettings,
		PointCloudSettings,
		MatrixSettings,
		PlotSettings,
		type GenericSettings
	} from '../settings/SettingsModel.js';
	import ImageSettingsPanel from './ImageSettingsPanel.svelte';
	import MatrixSettingsPanel from './MatrixSettingsPanel.svelte';
	import MetadataSettingsPanel from './MetadataSettingsPanel.svelte';
	import PlotSettingsPanel from './PlotSettingsPanel.svelte';
	import PointCloudSettingsPanel from './PointCloudSettingsPanel.svelte';

	export let userSettings: GenericSettings | null = null;
</script>

{#if userSettings}
	{#if userSettings instanceof ImageSettings}
		<ImageSettingsPanel bind:userSettings />
	{:else if userSettings instanceof MatrixSettings}
		<MatrixSettingsPanel bind:userSettings />
	{:else if userSettings instanceof MetadataSettings}
		<MetadataSettingsPanel bind:userSettings />
	{:else if userSettings instanceof PointCloudSettings}
		<PointCloudSettingsPanel bind:userSettings />
	{:else if userSettings instanceof PlotSettings}
		<PlotSettingsPanel bind:userSettings />
	{/if}
{/if}
