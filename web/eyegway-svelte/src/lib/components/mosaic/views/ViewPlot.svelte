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

	let relayouting: boolean = false;
	let relayout: boolean = false;

	function handleRelayouting(event: CustomEvent) {
		layout = deepMerge(layout, unflattenObject(event.detail));
		relayouting = true;
	}
	function handleRelayout(event: CustomEvent) {
		relayouting = false;
		layout = deepMerge(layout, unflattenObject(event.detail));
		relayout = true;
	}

	$: if (userData) {
		data = structuredClone(userData.data);
		if (!relayouting && !relayout) layout = structuredClone(userData.layout);
		config = structuredClone(userData.config);
	}
</script>

<Plot
	bind:data
	bind:layout
	bind:config
	fillParent={true}
	debounce={0}
	configReactivityStrategy={'none'}
	on:relayouting={handleRelayouting}
	on:restyle={handleRelayout}
	on:relayout={handleRelayout}
	on:afterPlot={handleRelayout}
/>
