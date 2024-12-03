<script lang="ts">
	import { PaneGroup, Pane, PaneResizer } from 'paneforge';
	import Tile from './Tile.svelte';
	import { onMount } from 'svelte';
	import type { PaneConfiguration } from './PaneModel.js';
	import { GripHorizontal, GripVertical } from 'lucide-svelte';
	import { paneConfiguration } from './PaneStore.js';

	export let pane: PaneConfiguration;
	export let editMode;
	export let dataStream;
	export let tips;

	function splitPane(direction: string) {
		pane.split = direction;
		pane.children = [
			{
				id: Date.now(),
				split: '',
				size: 50,
				children: [],
				item: { name: pane.item.name, settings: pane.item.settings } // Clone the item
			},
			{
				id: Date.now() + 1,
				split: '',
				size: 50,
				children: [],
				item: { name: '', settings: {} }
			}
		];
	}

	function handleSplit(event: CustomEvent<{ direction: string }>) {
		splitPane(event.detail.direction);
	}

	function handleDelete(event: CustomEvent) {
		removePane($paneConfiguration, pane);
	}

	// Recursive function to remove a pane from the tree
	function removePane(parentPane: PaneConfiguration, paneToDelete: PaneConfiguration) {
		if (!parentPane.children) return false;

		const index = parentPane.children.findIndex((child) => child.id === paneToDelete.id);
		if (index !== -1) {
			parentPane.children.splice(index, 1);
			if (parentPane.children.length === 1) {
				// Collapse parent pane if only one child remains
				const remainingChild = parentPane.children[0];
				parentPane.split = remainingChild.split;
				parentPane.children = remainingChild.children;
				parentPane.item = remainingChild.item;
			} else if (parentPane.children.length === 0) {
				parentPane.split = '';
				parentPane.item = { name: '', settings: {} };
			}
			return true;
		}

		// Recursively search in child panes
		for (let child of parentPane.children) {
			if (removePane(child, paneToDelete)) {
				return true;
			}
		}

		return false;
	}

	let resizing: boolean = false;

	onMount(() => {
		resizing = false;
	});

	function handleResize(child: PaneConfiguration, size: number, prevSize: number | undefined) {
		child.size = Math.round(size);
		pane = { ...pane }; // Trigger reactivity
		resizing = true;
	}
	function handleDraggingChange() {
		resizing = false;
	}
</script>

{#if pane.split}
	<PaneGroup
		style={editMode ? 'overflow: hidden;' : 'overflow: hidden'}
		{...{
			...{}
			/* @ts-ignore */
		}}
		direction={pane.split}
	>
		{#each pane.children as child (child.id)}
			<Pane
				defaultSize={child.size}
				style={editMode ? 'overflow: hidden;' : 'overflow: hidden'}
				{...{
					...{}
					/* @ts-ignore */
				}}
				onResize={(size, prevSize) => {
					handleResize(child, size, prevSize);
				}}
			>
				<svelte:self bind:pane={child} {editMode} {dataStream} {tips} on:deletePane on:resizePane />
			</Pane>
			{#if editMode}
				{#if pane.children.length > 1 && pane.children.indexOf(child) < pane.children.length - 1}
					<PaneResizer class="dots" onDraggingChange={handleDraggingChange}>
						{#if pane.split == 'vertical'}
							<div
								class="is-flex is-flex-direction-column is-align-items-center is-justify-content-center dots vertical"
							>
								<span class="percent">{resizing ? child.size + '%' : ''}</span>
								<div class="is-flex vertical">
									<GripHorizontal
										size={20}
										style="color: var(--bulma-scheme-main); background-color: var(--bulma-text-strong); border-radius: 4px;  z-index: 10; border: 2px solid var(--bulma-text);"
									/>
								</div>
								<span class="percent">{resizing ? 100 - child.size + '%' : ''}</span>
							</div>
						{:else}
							<div
								class=" is-flex is-flex-direction-row is-align-items-center is-justify-content-center dots horizontal"
							>
								<div class="is-flex horizontal">
									<span class="percent">{resizing ? child.size + '%' : ''}</span>
									<GripVertical
										size={20}
										style="color: var(--bulma-scheme-main); background-color: var(--bulma-text-strong); border-radius: 4px;  z-index: 10; border: 2px solid var(--bulma-text);"
									/>
									<span class="percent">{resizing ? 100 - child.size + '%' : ''}</span>
								</div>
							</div>
						{/if}
					</PaneResizer>
				{/if}
			{/if}
		{/each}
	</PaneGroup>
{:else}
	<Tile
		editable={editMode}
		{dataStream}
		bind:item={pane.item}
		{tips}
		on:splitPane={handleSplit}
		on:delete={handleDelete}
	/>
{/if}

<style>
	.dots {
		color: var(--color-header-buttons);
		width: 100%;
		height: 100%;
	}
	.dots.vertical {
		height: 2px;
		background: linear-gradient(
			to right,
			#ffffff00 0%,
			#ffffff00 14%,
			var(--color-header-buttons) 15%,
			var(--color-header-buttons) 85%,
			#ffffff00 86%,
			#ffffff00 100%
		);
	}
	.dots.horizontal {
		width: 2px;
		background: linear-gradient(
			to bottom,
			#ffffff00 0%,
			#ffffff00 14%,
			var(--color-header-buttons) 15%,
			var(--color-header-buttons) 85%,
			#ffffff00 86%,
			#ffffff00 100%
		);
	}
	.percent {
		font-size: 0.7em;
		font-weight: bold;
		padding-left: 5px;
		padding-right: 5px;
		z-index: 10;
		mix-blend-mode: exclusion;
		filter: invert();
	}
</style>
