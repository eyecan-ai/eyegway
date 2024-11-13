<script lang="ts">
	import { PaneGroup, Pane, PaneResizer } from 'paneforge';
	import Tile from './Tile.svelte';
	import { createEventDispatcher } from 'svelte';
	import type { PaneConfiguration } from './PaneModel.js';

	export let pane: PaneConfiguration;
	export let editMode;
	export let dataStream;
	export let tips;

	const dispatch = createEventDispatcher();

	function splitPane(direction: string) {
		pane.split = direction;
		pane.children = [
			{
				id: Date.now(),
				split: '',
				size: 50,
				children: [],
				item: { name: pane.item.name } // Clone the item
			},
			{
				id: Date.now() + 1,
				split: '',
				size: 50,
				children: [],
				item: { name: '' }
			}
		];
	}

	function handleSplitPane(event: CustomEvent<{ direction: string }>) {
		splitPane(event.detail.direction);
	}

	function handleDelete() {
		dispatch('deletePane', { pane });
	}
	function handleResize(child: PaneConfiguration, size: number, prevSize: number | undefined) {
		child.size = size;
	}
</script>

{#if pane.split}
	<PaneGroup
		style={editMode ? 'overflow: visible;' : ''}
		{...{
			...{}
			/* @ts-ignore */
		}}
		direction={pane.split}
	>
		{#each pane.children as child (child.id)}
			<Pane
				defaultSize={child.size}
				style={editMode ? 'overflow: visible;' : ''}
				onResize={(size, prevSize) => {
					handleResize(child, size, prevSize);
				}}
			>
				<svelte:self pane={child} {editMode} {dataStream} {tips} on:deletePane on:resizePane />
			</Pane>
			{#if pane.children.length > 1 && pane.children.indexOf(child) < pane.children.length - 1}
				<PaneResizer class="dots">
					{#if editMode}
						{#if pane.split == 'vertical'}
							<div
								class="is-z-index-1 is-flex is-align-items-center is-justify-content-center dots vertical"
							/>
						{:else}
							<div
								class="is-z-index-1 is-flex is-align-items-center is-justify-content-center dots horizontal"
							/>
						{/if}
					{/if}
				</PaneResizer>
			{/if}
		{/each}
	</PaneGroup>
{:else}
	<Tile
		editable={editMode}
		{dataStream}
		item={pane.item}
		{tips}
		on:splitPane={handleSplitPane}
		on:delete={handleDelete}
	/>
{/if}

<style>
	.dots {
		color: #b49e9e;
	}
	.dots.vertical {
		width: 100%;
		height: 10px;
	}
	.dots.horizontal {
		height: 100%;
		width: 10px;
	}
</style>
