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
	import ViewGeneric from './views/ViewGeneric.svelte';
	import { DataExtractor, type TileItem } from './PaneModel.js';
	import GenericSettingsPanel from './settings/GenericSettingsPanel.svelte';

	export let item: TileItem | null = null;
	export let dataStream: any | null = null;
	export let editable: boolean = false;
	export let tips: string[] = [];

	let extractedData: any | null = null;

	const dispatch = createEventDispatcher();

	function splitHorizontal() {
		dispatch('split', { direction: 'horizontal' });
	}

	function splitVertical() {
		dispatch('split', { direction: 'vertical' });
	}

	function onDelete() {
		selectTip('');
		dispatch('delete', item);
	}

	$: if (item) {
		selectedTip = item.name;
		extractedData = DataExtractor.pickAndParse(dataStream, item.name);
		item.settings = DataExtractor.getSettingsType(extractedData, item.settings);
	}

	let isDropdownOpen: boolean = false;
	let isSettingsOpen: boolean = false;
	let selectedTip: string = '';

	function selectTip(tip: string) {
		if (item) item.name = tip;
		selectedTip = tip;
		isDropdownOpen = false;
		dispatch('update');
	}
</script>

<div class="tile-content">
	{#if editable}
		<!-- Editable Mode -->
		<div class="item-editable {item?.name ? 'card panel' : 'panel-empty'}">
			<div class="item-preview">
				<div class="blur-content">
					{#if item?.name}
						<ViewGeneric userData={extractedData} userSettings={item.settings} />
					{/if}
				</div>
			</div>
			<div class="columns">
				<div class="column content">
					<div class="dropdown" class:is-active={isDropdownOpen}>
						<div class="dropdown-trigger">
							<button
								class="button is-small is-fullwidth"
								aria-haspopup="true"
								aria-controls="dropdown-menu"
								on:click={() => (isDropdownOpen = !isDropdownOpen)}
							>
								<span class="ellipsis-text">{selectedTip || 'select data'}</span>
								<span class="icon is-small">
									<ArrowDown size={12} />
								</span>
							</button>
						</div>
						<div class="dropdown-menu" id="dropdown-menu" role="menu">
							<div class="dropdown-content">
								<a
									href={'#'}
									class="dropdown-item has-text-danger is-flex is-justify-content-right"
									on:click={() => selectTip('')}
								>
									<X size={12} />
								</a>
								{#each tips as tip}
									<a
										href={'#'}
										class="dropdown-item {tip == selectedTip ? 'is-active' : ''} "
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
						class="button is-small is-info"
						on:click={splitHorizontal}
						title="Split horizontally"
					>
						<SplitSquareHorizontal size={16} />
					</button>
				</div>
				<div class="column control-item is-narrow">
					<button class="button is-small is-info" on:click={splitVertical} title="Split vertically">
						<SplitSquareVertical size={16} />
					</button>
				</div>
				<div class="column control-item is-narrow">
					<div class="dropdown is-right is-down {isSettingsOpen ? 'is-active' : ''}">
						<div class="dropdown-trigger">
							<button
								class="button is-small is-warning"
								disabled={item?.name ? false : true}
								aria-haspopup="true"
								aria-controls="dropdown-menu4"
								class:is-inverted={isSettingsOpen}
								on:click={() => (isSettingsOpen = !isSettingsOpen)}
							>
								<Cog size={16} />
							</button>
						</div>
						<div class="dropdown-menu" id="dropdown-menu4" role="menu">
							<!-- <div class="dropdown-content"> -->
							{#if item?.name}
								<GenericSettingsPanel bind:userSettings={item.settings} />
							{/if}
							<!-- </div> -->
						</div>
					</div>
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
		<div class="item {item?.name ? 'card panel' : ''}">
			{#if item?.name}
				<ViewGeneric userData={extractedData} userSettings={item.settings} />
			{/if}
		</div>
	{/if}
</div>

<style>
	.panel {
		background-color: rgba(
			var(--eyegway-panel-background-color-r),
			var(--eyegway-panel-background-color-g),
			var(--eyegway-panel-background-color-b),
			var(--eyegway-panel-background-color-a)
		);
	}
	.panel-empty {
		border-radius: 10px;
		background-color: 'transparent';
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

	.button {
		white-space: wrap;
	}

	.item-preview {
		display: grid;
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		border-radius: 10px;
		overflow: hidden;
	}
	.item-preview .blur-content {
		display: grid;
		filter: blur(5px) contrast(0.5);
	}

	.item {
		display: grid;
		width: 100%;
		height: 100%;
		border-radius: 10px;
	}

	.dropdown-content {
		position: fixed;
	}
</style>
