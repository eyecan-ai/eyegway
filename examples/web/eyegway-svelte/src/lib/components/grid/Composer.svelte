<script lang="ts">
	import Grid, { type GridController } from 'svelte-grid-extended';
	import ItemPlaceholder from './ItemPlaceholder.svelte';
	import { EyegwayDataPurger, ProtoypeItem } from './Data.js';
	import DataItem from './DataItem.svelte';

	export let gridSize: [number, number] = [16, 16];
	export let height: number = 400;
	export let sharedData: any = {};
	let purgedData: any = {};
	let gridController: GridController;
	let editableMode: boolean = true;

	let items = [new ProtoypeItem('[placeholder]', 0, 0, 2, 2)];

	function addNewItem() {
		const pos = gridController.getFirstAvailablePosition(2, 2);
		if (pos == null) {
			return;
		} else {
			items = [...items, new ProtoypeItem('[placeholder]', pos.x, pos.y, 2, 2)];
		}
	}

	function removeItem(event: CustomEvent<ProtoypeItem>) {
		console.log('remove', event.detail);
		items = items.filter((item) => item !== event.detail);
	}

	$: if (sharedData) {
		purgedData = EyegwayDataPurger.purge(sharedData);
	}
</script>

<div class="box">
	<button class="button is-primary" on:click={addNewItem}>Add new item</button>
	<button class="button is-primary" on:click={() => (editableMode = !editableMode)}>
		{editableMode ? 'View' : 'Edit'}
	</button>
</div>
<div
	class="container composer-container box grid-container editable p-0 mt-0"
	style="height:{height}px;"
>
	{#if editableMode}
		<Grid cols={gridSize[1]} rows={gridSize[0]} bind:controller={gridController}>
			{#each items as item}
				<ItemPlaceholder
					bind:prototype={item}
					tips={Object.keys(purgedData)}
					on:delete={removeItem}
				/>
			{/each}
		</Grid>
	{:else}
		<Grid cols={gridSize[1]} rows={gridSize[0]} readOnly>
			{#each items as item}
				<DataItem bind:prototype={item} data={purgedData} />
			{/each}
		</Grid>
	{/if}
</div>

<style>
</style>
