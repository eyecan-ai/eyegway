<script lang="ts">
	import { JSONEditor } from 'svelte-jsoneditor';

	let metadata: any = {
		detections: [
			{ x: 1, y: 1, z: 3 },
			{ x: 2, y: 2, z: 3 },
			{ x: 3, y: 3, z: 3 }
		]
	};
	export let key: string = 'detections';
	export let query: string = parseQueryString('[ x:${x}, y:${y}, z:${z}]');

	let items: any[] = [];

	/**
	 * This function parses the query string and replace all custom tags like <red>
	 * with the corresponding HTML tag. For example:
	 *
	 * <red> -> <span style="color: red;">
	 * <blue> -> <span style="color: blue;">
	 * <green> -> <span style="color: green;">
	 * <#ff0000> -> <span style="color: #ff0000;">
	 * <#00ff00> -> <span style="color: #00ff00;">
	 * and so on...
	 */
	function parseQueryString(query: string) {
		return query.replace(/<(\w+)>/g, (match, p1) => {
			if (p1.startsWith('#')) {
				return `<span style="color: ${p1};">`;
			} else {
				return `<span class="${p1}">`;
			}
		});
	}

	$: if (metadata) {
		console.log('MetadataCustom', metadata);
		let chunk;
		if (key === '*') {
			chunk = metadata;
		} else {
			chunk = metadata[key];
		}
		console.log('Chunk', chunk);
		if (chunk instanceof Array) {
			items = chunk;
		} else {
			items = [chunk];
		}
		console.log('MetadataCustom', metadata);
	}
</script>

{#each items as item}
	<div class="box">
		{#if query === '*'}
			{JSON.stringify(item)}
		{:else}
			{@html `${query}`.replace(/\${(\w+)}/g, (match, p1) => item[p1].toFixed(2))}
			<!-- {@html html} -->
		{/if}
	</div>
{/each}

<style>
	red {
		color: red;
	}
</style>
