<script lang="ts">
	import Plot from 'svelte-plotly.js';
	import type { Layout, Data, Config } from 'plotly.js';
	import type { DataPlot } from '../MosaicModel.js';

	export let userData: DataPlot | null = null;

	let relayouting: boolean = false;
	let relayout: boolean = false;

	function parseObject<T>(obj: any, template: T): T {
		const result: Partial<T> = {};
		for (const key in template) {
			if (obj.hasOwnProperty(key) && typeof obj[key] === typeof template[key]) {
				result[key] = obj[key];
			}
		}
		return result as T;
	}

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

	$: if (userData && !relayouting) {
		data = userData.data;
		if (!relayout) layout = parseObject(userData.layout, layout);
		config = parseObject(userData.config, config);
	}
	function handleRelayouting(event: CustomEvent) {
		relayouting = true;
	}
	function handleRelayout(event: CustomEvent) {
		layout = deepMerge(layout, unflattenObject(event.detail));
		relayouting = false;
		relayout = true;
	}
</script>

{#if userData}
	<Plot
		{data}
		{layout}
		{config}
		fillParent={true}
		debounce={1}
		configReactivityStrategy={'none'}
		on:relayouting={handleRelayouting}
		on:relayout={handleRelayout}
	/>
{/if}
