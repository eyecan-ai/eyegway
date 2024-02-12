<script lang="ts">
	import Grid, { type GridController } from 'svelte-grid-extended';
	import { MosaicConfiguration, MosaicItem } from './MosaicModel.js';
	import MosaicTile from './MosaicTile.svelte';
	import { MosaicConfigurationsUtils } from './MosaicUtils.js';
	import { onMount } from 'svelte';

	export let size: [number, number] = [16, 16];
	export let controls: boolean = true;
	export let autoLoadDefault: boolean = true;
	export let editableMode: boolean = true;
	export let defaultKey: string = '[placeholder]';
	export let items: MosaicItem[] = [];
	export let height: number = 600;
	export let data: any = {};
	let newItemSize: [number, number] = [5, 5];
	let gridController: GridController;

	/**
	 * Add a new item to the grid. It can be called from the parent component.
	 */
	export function newItem() {
		const pos = gridController.getFirstAvailablePosition(newItemSize[0], newItemSize[1]);
		if (pos == null) {
			return;
		} else {
			items = [...items, new MosaicItem(defaultKey, pos.x, pos.y, newItemSize[0], newItemSize[1])];
		}
	}

	/**
	 * Export the current configuration. It can be called from the parent component.
	 */
	export function exportConfiguration(): MosaicConfiguration {
		const configuration = new MosaicConfiguration(items, size);
		return configuration;
	}

	/**
	 * Save the configuration to a file. It can be called from the parent component.
	 */
	export function saveConfigurationToFile() {
		const configuration = exportConfiguration();
		MosaicConfigurationsUtils.saveConfigurationToFile(configuration);
	}

	/**
	 * Load the configuration from a file. It can be called from the parent component.
	 */
	export async function loadConfigurationFromFile() {
		const configuration = await MosaicConfigurationsUtils.loadConfigurationFromFile();
		reloadConfiguration(configuration);
	}

	/**
	 * Save the configuration as default. It can be called from the parent component.
	 */
	export function saveConfigurationAsDefault() {
		const configuration = exportConfiguration();
		MosaicConfigurationsUtils.saveConfigurationAsDefault(configuration);
	}

	/**
	 * Load the default configuration. It can be called from the parent component.
	 */
	export function loadDefaultConfiguration() {
		const configuration = MosaicConfigurationsUtils.loadDefaultConfiguration();
		if (configuration) reloadConfiguration(configuration);
	}

	/**
	 * Reload the configuration. It can be called from the parent component.
	 */
	export function reloadConfiguration(configuration: MosaicConfiguration) {
		items = configuration.items;
		size = configuration.size;
	}

	/**
	 * Clear the grid. It can be called from the parent component.
	 */
	export function clear() {
		items = [];
	}

	/**
	 * Toggle the editable mode. It can be called from the parent component.
	 */
	export function toggleEditableMode() {
		editableMode = !editableMode;
	}

	/**
	 * Check if the grid is in editable mode. It can be called from the parent component.
	 */
	export function isEditable() {
		return editableMode;
	}

	/**
	 * On delete item event, remove the item from the grid. It is called from any
	 * MosaicTile component.
	 * @param event CustomEvent<MosaicItem>
	 */
	function onDeleteItem(event: CustomEvent<MosaicItem>) {
		console.log('remove', event.detail);
		items = items.filter((item) => item !== event.detail);
	}

	onMount(() => {
		if (autoLoadDefault) {
			loadDefaultConfiguration();
		}
	});

	$: {
		if (size) {
			newItemSize = [Math.floor(size[0] / 4), Math.floor(size[1] / 4)];
		}
	}
</script>

<div class="p-0" style="height:{height}px;">
	<Grid cols={size[1]} rows={size[0]} bind:controller={gridController} readOnly={!editableMode}>
		{#if items.length == 0}
			<div class="notification m-4 no-items">No items, add one ...</div>
		{/if}
		{#each items as item}
			<MosaicTile
				bind:item
				tips={data ? Object.keys(data) : []}
				editable={editableMode}
				dataStream={data}
				on:delete={onDeleteItem}
			/>
		{/each}
	</Grid>
</div>
{#if controls}
	<div class="controls p-2">
		<div class="columns">
			<div class="column is-narrow">
				<button
					class="button is-small is-outlined"
					class:is-primary={editableMode}
					class:is-warning={!editableMode}
					on:click={toggleEditableMode}
				>
					{editableMode ? 'Play' : 'Edit'}
				</button>
				{#if editableMode}
					<button class="button is-small is-outlined is-primary" on:click={newItem}>
						New Item
					</button>
					<button class="button is-small is-outlined is-danger" on:click={clear}> Clear </button>
				{/if}
			</div>
			{#if editableMode}
				<div class="column is-narrow">|</div>
				<div class="column is-narrow">
					<!-- SAVE TO FILE-->
					<button
						class="button is-small is-outlined is-info"
						disabled={items.length == 0}
						on:click={saveConfigurationToFile}
					>
						Save to file
					</button>

					<!-- LOAD FROM FILE-->
					<button class="button is-small is-outlined is-info" on:click={loadConfigurationFromFile}>
						Load from file
					</button>

					<!-- SAVE AS DEFAULT-->
					<button
						class="button is-small is-outlined is-info"
						disabled={items.length == 0}
						on:click={saveConfigurationAsDefault}
					>
						Save as default
					</button>

					<!-- LOAD DEFAULT-->
					<button class="button is-small is-outlined is-info" on:click={loadDefaultConfiguration}>
						Load default
					</button>
				</div>
			{/if}
		</div>
	</div>
{/if}

<style>
	.no-items {
		margin-top: 100px;
		position: absolute;
	}
	.controls {
		border-top: 1px dashed #eee;
	}
</style>
