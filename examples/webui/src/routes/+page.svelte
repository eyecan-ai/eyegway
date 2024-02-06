<script lang="ts">
	import Item from '$lib/components/Item.svelte';
	import ItemPlaceholder from '$lib/components/ItemPlaceholder.svelte';
	import { ProtoypeItem } from '$lib/components/items/DynamicGrid';
	import { CustomConnector, EImage, EPointCloud } from '$lib/eyegway/CustomConnector';
	import { EyegwayClient } from '$lib/eyegway/EyegwayClient';
	import { onMount } from 'svelte';
	import Grid, { GridItem, type GridController } from 'svelte-grid-extended';

	console.log('ciao');

	let sharedData: any = {};
	let sharedDataOffset: number = 0;
	let ready: boolean = true;
	let editableMode: boolean = true;

	// GRID
	let gridSize: number[] = [8, 8];
	let gridController: GridController;

	let items = [new ProtoypeItem('[placeholder]', 0, 0, 2, 2)];

	function addNewItem() {
		const pos = gridController.getFirstAvailablePosition(2, 2);
		if (pos == null) {
			console.log('No space');
			return;
		} else {
			console.log('Space', pos);
			items = [...items, new ProtoypeItem('[placeholder]', pos.x, pos.y, 2, 2)];
		}
	}

	function removeItem(event: CustomEvent<ProtoypeItem>) {
		console.log('remove', event.detail);
		items = items.filter((item) => item !== event.detail);
	}

	function changeOffset(delta: number) {
		sharedDataOffset += delta;
		if (sharedDataOffset < 0) sharedDataOffset = 0;
		updateData();
	}

	async function updateData() {
		const hubName = 'fai4ba';
		const client = EyegwayClient.getInstance();
		client.setConnector(new CustomConnector());
		sharedData = await client.last(hubName, sharedDataOffset);
		console.log(sharedData);
		ready = true;
	}

	onMount(async () => {
		await updateData();
	});
</script>

<div class="container box mt-2">
	{#if editableMode}
		<div class="columns">
			<div class="column is-narrow">
				<button
					class="button is-small is-primary is-outlined"
					on:click={() => (editableMode = false)}>Run View</button
				>
			</div>
			<div class="column is-narrow">|</div>
			<div class="column is-narrow">
				<button class="button is-small is-success" on:click={addNewItem}>New Item</button>
				<button
					class="button is-small is-danger"
					on:click={() => {
						items = [];
					}}>Clear</button
				>
			</div>
		</div>
	{:else}
		<div class="columns is-vcentered">
			<button class="button is-small is-warning is-outlined" on:click={() => (editableMode = true)}
				>Edit Grid</button
			>
			<div class="column is-narrow">|</div>
			<div class="column is-narrow">
				<button class="button is-small is-success" on:click={() => changeOffset(-1)}>Prev.</button>
				<button class="button is-small is-success" disabled>{sharedDataOffset}</button>
				<button class="button is-small is-success" on:click={() => changeOffset(1)}>Next.</button>
			</div>
		</div>
	{/if}
</div>
{#if editableMode}
	<div class="container box grid-container editable p-0 mt-0">
		<Grid cols={gridSize[1]} rows={gridSize[0]} bind:controller={gridController}>
			{#each items as item}
				<ItemPlaceholder
					bind:prototype={item}
					tips={Object.keys(sharedData)}
					on:delete={removeItem}
				/>
			{/each}
		</Grid>
	</div>
{:else}
	<div class="container box grid-container p-0 mt-0">
		<Grid cols={gridSize[1]} rows={gridSize[0]} readOnly>
			{#each items as item}
				<Item bind:prototype={item} data={sharedData} />
			{/each}
		</Grid>
	</div>
{/if}

<style>
	.grid-container {
		height: 600px;
		background-color: #eee;
	}
	.grid-container.editable {
		background-color: #ddd;
	}
</style>
