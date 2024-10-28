<script lang="ts">
	import Plot from 'svelte-plotly.js';
	import type { DataPlot } from '../MosaicModel.js';

	export let userData: DataPlot | null = null;

	$: if (userData) {
		console.log(userData);
	}
	// $: if (userData) {
	// Extract data from EyegwayTensor

	// data = [
	// 	{
	// 		// x: userData.x.data,
	// 		// y: userData.y.data,
	// 		x: [1, 2, 3, 4, 5],
	// 		y: [0.1, 0.15, 0.13, 0.17, 0.22],
	// 		type: userData.options.type || 'scatter',
	// 		mode: userData.options.mode || 'lines+markers',
	// 		marker: userData.options.marker || {},
	// 		line: userData.options.line || {},
	// 		name: userData.options.name || ''
	// 	}
	// ];

	// layout = {
	// 	title: userData.options.title || '',
	// 	xaxis: userData.options.xaxis || {},
	// 	yaxis: userData.options.yaxis || {},
	// 	margin: { t: 0 },
	// 	...userData.options.layout
	// };

	// console.log('Plot data:', data);
	// console.log('Plot layout:', layout);
	// }
</script>

{#if userData}
	<Plot
		data={userData.data}
		layout={userData.layout}
		config={userData.config}
		fillParent={true}
		debounce={250}
	/>
{/if}
