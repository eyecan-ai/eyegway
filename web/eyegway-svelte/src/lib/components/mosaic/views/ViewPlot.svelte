<script lang="ts">
	import Plot from 'svelte-plotly.js';
	import type { DataPlot } from '../MosaicModel.js';

	export let userData: DataPlot | null = null;
</script>

<div class="plot_container">
	<Plot
		data={userData?.data}
		layout={userData?.layout}
		config={userData?.config}
		fillParent={true}
		debounce={0}
		configReactivityStrategy={'none'}
	/>
</div>

<style>
	.plot_container {
		border-radius: 10px;
	}
</style>
