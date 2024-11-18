<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import {
		SplitSquareHorizontal,
		SplitSquareVertical,
		Trash,
		Cog,
		ArrowDown,
		X
	} from 'lucide-svelte';
	import ViewGeneric from '../mosaic/views/ViewGeneric.svelte';
	import { DataExtractor } from '../mosaic/MosaicModel.js';
	import { TileItem } from './PaneModel.js';

	export let item: TileItem | null = null;
	export let dataStream: any | null = null;
	export let editable: boolean = false;
	export let tips: string[] = [];

	const dispatch = createEventDispatcher();

	// Extracted data based on item.name
	let extractedData: any | null = null;

	// Re-compute extractedData when item or dataStream changes
	$: if (item && dataStream) {
		if (!isDropdownOpen) selectTip(item.name);
		extractedData = DataExtractor.pickAndParse(dataStream, item.name);
	}

	// Functions to handle splitting
	function splitHorizontal() {
		dispatch('splitPane', { direction: 'horizontal' });
	}

	function splitVertical() {
		dispatch('splitPane', { direction: 'vertical' });
	}

	function onDelete() {
		clearTip();
		dispatch('delete', item);
	}

	$: if (item && selectedTip) {
		item.name = selectedTip;
	}

	let isDropdownOpen: boolean = false;
	let selectedTip: string = '';

	function selectTip(tip: string) {
		selectedTip = tip;
		isDropdownOpen = false;
		// Handle the selected tip
	}
	function clearTip() {
		if (item) item.name = '';
		selectedTip = '';
		isDropdownOpen = false;
	}
</script>

<div class="tile-content">
	{#if editable}
		<!-- Editable Mode -->
		<div class="item-editable {item?.name ? 'card' : 'card-empty'}">
			<div class="columns">
				<div class="column content">
					<div class="dropdown" class:is-active={isDropdownOpen}>
						<div class="dropdown-trigger">
							<button
								class="button is-small is-dark is-fullwidth"
								aria-haspopup="true"
								aria-controls="dropdown-menu"
								on:click={() => (isDropdownOpen = !isDropdownOpen)}
							>
								<span>{selectedTip || 'select data'}</span>
								<span class="icon is-small">
									<ArrowDown size={12} />
								</span>
							</button>
						</div>
						<div class="dropdown-menu" id="dropdown-menu" role="menu">
							<div class="dropdown-content has-background-dark">
								<!--svelte: -->
								<a
									href={'#'}
									class="dropdown-item has-text-danger is-flex is-justify-content-right"
									on:click={() => clearTip()}
								>
									<X size={12} />
								</a>
								{#each tips as tip}
									<a
										href={'#'}
										class="dropdown-item has-text-white {tip == selectedTip ? 'is-active' : ''} "
										on:click={() => selectTip(tip)}
									>
										{tip}
									</a>
								{/each}
							</div>
						</div>
					</div>
				</div>
			</div>
			<div class="columns is-multiline controls is-mobile is-centered">
				<div class="column control-item is-narrow">
					<button
						class="button is-small is-light is-info"
						on:click={splitHorizontal}
						title="Split horizontally"
					>
						<SplitSquareHorizontal size={16} />
					</button>
				</div>
				<div class="column control-item is-narrow">
					<button
						class="button is-small is-light is-info"
						on:click={splitVertical}
						title="Split vertically"
					>
						<SplitSquareVertical size={16} />
					</button>
				</div>
				<div class="column control-item is-narrow">
					<button
						class="button is-small is-light"
						on:click={() => console.log('Edit')}
						title="Settings"
					>
						<Cog size={16} />
					</button>
				</div>
				<div class="column control-item is-narrow">
					<button class="button is-small is-danger" on:click={onDelete} title="Delete Tile">
						<Trash size={16} />
					</button>
				</div>
			</div>
		</div>
	{:else}
		<!-- Display Mode -->
		<div class="item {item?.name ? 'card' : ''}">
			{#if item?.name}
				<ViewGeneric userData={extractedData} />
			{/if}
		</div>
	{/if}
</div>

<style>
	.card {
		border-radius: 10px;
		background-color: var(--color-panel);
	}
	.card-empty {
		border-radius: 10px;
		/* border: 2px dashed var(--color-panel-unselected); */
		background-color: var(--color-panel-unselected);
	}
	.dropdown-item {
		padding-right: 10px;
	}
	.control-item {
		padding: 0.1em;
	}
	.tile-content {
		display: flex;
		position: relative;
		width: 100%;
		height: 100%;
		align-items: center;
		justify-content: center;
		padding: 8px;
		border-radius: 10px;
	}

	.item-editable {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		padding: 8px;
		align-items: center;
		justify-content: center;
	}

	.item-editable .controls {
		display: flex;
	}

	.item-editable .content {
		flex-grow: 1;
	}

	.item {
		display: grid;
		width: 100%;
		height: 100%;
		border-radius: 10px;
	}
</style>
