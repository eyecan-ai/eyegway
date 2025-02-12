<script lang="ts">
	import Plot from 'svelte-plotly.js';
	import type { DataPlot } from '../PaneModel.js';
	import type { PlotSettings } from '../settings/SettingsModel.js';

	export let userData: DataPlot | null = null;
	export let userSettings: PlotSettings | null = null;
</script>

{#if userData && userSettings}
	<div class="plot_container">
		<Plot
			data={userData.data}
			layout={userData.layout}
			config={userData.config}
			fillParent={userSettings.fillParent}
			debounce={userSettings.debounce}
			configReactivityStrategy={'none'}
		/>
	</div>
{/if}

<style>
	.plot_container {
		border-radius: 10px;
	}
</style>
