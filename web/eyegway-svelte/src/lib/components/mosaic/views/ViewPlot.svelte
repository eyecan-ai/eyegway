<script lang="ts">
	import Plot from 'svelte-plotly.js';
	import type { Layout, Data, Config } from 'plotly.js';
	import type { DataPlot } from '../MosaicModel.js';

	export let userData: DataPlot | null = null;

	function unflattenObject(data: any) {
		const result: any = {};
		for (const key in data) {
			const keys = key.split('.');
			keys.reduce((acc: any, curr: string, index: number) => {
				if (index === keys.length - 1) {
					acc[curr] = data[key];
				} else {
					acc[curr] = acc[curr] || {};
				}
				return acc[curr];
			}, result);
		}
		return result;
	}

	function deepMerge(target: any, source: any) {
		for (const key in source) {
			if (source[key] instanceof Object && key in target) {
				target[key] = deepMerge(target[key], source[key]);
			} else {
				target[key] = source[key];
			}
		}
		return target;
	}

	let data: Data[] = [];
	let layout: Partial<Layout> = {};
	let config: Partial<Config> = {};

	let updating: boolean = false;
	let update: boolean = false;

	function handleLocalUpdate(event: CustomEvent) {
		layout = deepMerge(layout, unflattenObject(event.detail));
		updating = event.type === 'relayouting';
		update = !updating;
	}

	$: if (userData) {
		data = structuredClone(userData.data);
		if (!updating && !update) layout = structuredClone(userData.layout);
		config = structuredClone(userData.config);
	}
</script>

<div class="plot_container">
	<Plot
		bind:data
		bind:layout
		bind:config
		fillParent={true}
		debounce={0}
		configReactivityStrategy={'none'}
		on:relayouting={handleLocalUpdate}
		on:restyle={handleLocalUpdate}
		on:relayout={handleLocalUpdate}
		on:afterPlot={handleLocalUpdate}
	/>
</div>

<style>
	.plot_container {
		border-radius: 10px;
	}
</style>
