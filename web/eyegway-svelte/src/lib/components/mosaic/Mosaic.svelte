<script lang="ts">
	import Grid, { type GridController } from 'svelte-grid-extended';
	import { MosaicConfiguration, MosaicItem } from './MosaicModel.js';
	import MosaicTile from './MosaicTile.svelte';
	import { MosaicConfigurationsUtils } from './MosaicUtils.js';
	import { onMount } from 'svelte';
	import {
		IconPlus,
		IconEdit,
		IconEditOff,
		IconDotsVertical,
		IconTrash,
		IconDeviceFloppy,
		IconDownload,
		IconUpload,
		IconHistory
	} from '@tabler/icons-svelte';

	export let defaultSize: [number, number] = [64, 64];
	export let controls: boolean = true;
	export let autoLoadDefault: boolean = true;
	export let editableMode: boolean = true;
	export let defaultHeight: number = 600;
	export let defaultKey: string = '[placeholder]';
	export let items: MosaicItem[] = [];
	export let data: any = {};
	let size: [number, number] = defaultSize;
	let height: number = defaultHeight;
	let newItemSize: [number, number] = [5, 5];
	let gridController: GridController;
	let disabled: boolean = false;

	/**
	 * Add a new item to the grid. It can be called from the parent component.
	 */
	export function newItem() {
		const pos = gridController.getFirstAvailablePosition(newItemSize[0], newItemSize[1]);
		console.log(newItemSize, size);
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
		const configuration = new MosaicConfiguration(items, size, height);
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
		disabled = true;
		items = configuration.items;
		size = configuration.size;
		height = configuration.height ? configuration.height : defaultHeight;
		setTimeout(() => {
			disabled = false;
		}, 100);
	}

	/**
	 * Clear the grid. It can be called from the parent component.
	 */
	export function clear() {
		disabled = true;
		items = [];
		size = defaultSize;
		height = defaultHeight;
		setTimeout(() => {
			disabled = false;
		}, 100);
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

<div class="mosaic">
	<div class="p-0" style="height:{height}px;">
		{#if items.length == 0}
			<div class="notification m-4 no-items">No items, add one ...</div>
		{/if}
		{#if !disabled}
			<Grid cols={size[0]} rows={size[1]} bind:controller={gridController} readOnly={!editableMode}>
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
		{/if}
	</div>
	{#if controls}
		<div class="controls p-2" class:controls-hidden={!editableMode}>
			<div class="columns is-vcentered is-variable is-1">
				<div class="column is-narrow">
					<button
						class="button is-warning is-small"
						on:click={toggleEditableMode}
						title="{editableMode ? 'Disable' : 'Enable'} Edit Mode"
					>
						{#if !editableMode}
							<IconEdit size={16} />
						{:else}
							<IconEditOff size={16} />
						{/if}
					</button>
				</div>
				{#if editableMode}
					<div class="column is-narrow">
						<IconDotsVertical size={16} />
					</div>
					<div class="column is-narrow">
						<button
							class="button is-small is-inverted is-primary"
							on:click={newItem}
							title="Add new item"
						>
							<IconPlus stroke={1} size={18} />
						</button>
						<button
							class="button is-small is-inverted is-danger"
							on:click={clear}
							title="Clear all items"
						>
							<IconTrash stroke={1} size={18} />
						</button>
					</div>
					<div class="column is-narrow">
						<IconDotsVertical size={16} />
					</div>
					<div class="column is-narrow">
						<!-- SAVE TO FILE-->
						<button
							class="button is-small is-info is-inverted"
							disabled={items.length == 0}
							on:click={saveConfigurationToFile}
							title="Download current Configuration to File"
						>
							<IconDownload stroke={1} size={18} />
						</button>

						<!-- LOAD FROM FILE-->
						<button
							class="button is-small is-inverted is-info"
							on:click={loadConfigurationFromFile}
							title="Load Configuration from File"
						>
							<IconUpload stroke={1} size={18} />
						</button>

						<!-- SAVE AS DEFAULT-->
						<button
							class="button is-small is-inverted is-info"
							disabled={items.length == 0}
							on:click={saveConfigurationAsDefault}
							title="Save as Default Configuration"
						>
							<IconDeviceFloppy stroke={1} size={18} />
						</button>

						<!-- LOAD DEFAULT-->
						<button
							class="button is-small is-inverted is-info"
							on:click={loadDefaultConfiguration}
							title="Reload Default Configuration"
						>
							<IconHistory stroke={1} size={18} />
						</button>
					</div>
					<div class="column is-narrow">
						<IconDotsVertical size={16} />
					</div>
					<div class="column is-narrow">
						<input
							class="input is-small"
							type="number"
							orient="vertical"
							placeholder="Height"
							min="400"
							max="1000"
							bind:value={height}
							title="Grid Height in Pixels"
						/>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.no-items {
		margin-top: 100px;
		position: absolute;
	}
	.mosaic .controls-hidden {
		display: none;
	}
	.mosaic:hover .controls-hidden {
		display: block;
	}
	.controls {
		border-top: 1px dashed #eee;
	}

	/** add global */

	:global(.float-container .float) {
		opacity: 0.1;
	}
	:global(.float-container:hover .float) {
		opacity: 1;
	}
	:global(.float:hover) {
		transform: scale(1.1);
		cursor: pointer;
	}
	:global(.float) {
		position: absolute;
		right: -10px;
		top: -10px;
		z-index: 1000;
	}
</style>
