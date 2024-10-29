<script lang="ts">
	import Plot from 'svelte-plotly.js';
	import type { Layout, Data, Config } from 'plotly.js';
	import type { DataPlot } from '../MosaicModel.js';

	export let userData: DataPlot | null = null;

	function parseObject<T>(obj: any, template: T): T {
		const result: Partial<T> = {};
		for (const key in template) {
			if (obj.hasOwnProperty(key) && typeof obj[key] === typeof template[key]) {
				result[key] = obj[key];
			}
		}
		return result as T;
	}

	let data: Data[] = [];
	let layout: Partial<Layout> = {};
	let config: Partial<Config> = {};
	$: if (userData) {
		data = userData.data;
		layout = parseObject(userData.layout, layout);
		config = parseObject(userData.config, config);
	}
</script>

{#if userData}
	<Plot {data} {layout} {config} fillParent={true} debounce={0} configReactivityStrategy={'none'} />
{/if}
