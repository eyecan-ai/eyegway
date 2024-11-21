<script lang="ts">
	import { PaneGroup, Pane, PaneResizer } from 'paneforge';
	import Tile from './Tile.svelte';
	import { createEventDispatcher, onMount } from 'svelte';
	import type { PaneConfiguration } from './PaneModel.js';
	import { GripHorizontal, GripVertical } from 'lucide-svelte';

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

	function handleSplitPane(event: CustomEvent<{ direction: string }>) {
		splitPane(event.detail.direction);
	}

	function handleDelete() {
		dispatch('deletePane', { pane });
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
		style="overflow: hidden;"
		{...{
			...{}
			/* @ts-ignore */
		}}
		direction={pane.split}
	>
		{#each pane.children as child (child.id)}
			<Pane
				defaultSize={child.size}
				style="overflow: hidden;"
				{...{
					...{}
					/* @ts-ignore */
				}}
				onResize={(size, prevSize) => {
					handleResize(child, size, prevSize);
				}}
			>
				<svelte:self pane={child} {editMode} {dataStream} {tips} on:deletePane on:resizePane />
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
										style="background-color: var(--color-panel); border-radius: 4px;  z-index: 10; border: 2px solid var(--color-header-buttons);"
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
										style="background-color: var(--color-panel); border-radius: 4px;  z-index: 10; border: 2px solid var(--color-header-buttons);"
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
		item={pane.item}
		{tips}
		on:splitPane={handleSplitPane}
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
