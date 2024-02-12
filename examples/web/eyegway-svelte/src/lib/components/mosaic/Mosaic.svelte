<script lang="ts">
	import Grid, { type GridController } from 'svelte-grid-extended';
	import { MosaicItem } from './MosaicModel.js';
	import MosaicTile from './MosaicTile.svelte';

	export let size: [number, number] = [16, 16];
	export let defaultKey: string = '[placeholder]';
	export let items: MosaicItem[] = [];
	export let height: number = 600;
	export let data: any = {};
	let newItemSize: [number, number] = [5, 5];
	let gridController: GridController;
	let editableMode: boolean = true;

	function newItem() {
		const pos = gridController.getFirstAvailablePosition(newItemSize[0], newItemSize[1]);
		if (pos == null) {
			return;
		} else {
			items = [...items, new MosaicItem(defaultKey, pos.x, pos.y, newItemSize[0], newItemSize[1])];
		}
	}

	function deleteItem(event: CustomEvent<MosaicItem>) {
		console.log('remove', event.detail);
		items = items.filter((item) => item !== event.detail);
	}

	$: {
		if (size) {
			newItemSize = [Math.floor(size[0] / 4), Math.floor(size[1] / 4)];
		}
	}
</script>

<div class="box">
	<button class="button is-primary" on:click={newItem}>Add new item</button>
	<button class="button is-primary" on:click={() => (editableMode = !editableMode)}>
		{editableMode ? 'View' : 'Edit'}
	</button>
</div>
<div class="container box p-0" style="height:{height}px;">
	<Grid cols={size[1]} rows={size[0]} bind:controller={gridController} readOnly={!editableMode}>
		{#each items as item}
			<MosaicTile
				bind:item
				tips={Object.keys(data)}
				editable={editableMode}
				dataStream={data}
				on:delete={deleteItem}
			/>
		{/each}
	</Grid>
</div>

<style>
</style>
