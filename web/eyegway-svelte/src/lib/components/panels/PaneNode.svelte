<script lang="ts">
	import { PaneGroup, Pane, PaneResizer, type PaneAPI } from 'paneforge';
	import Tile from './Tile.svelte';
	import { type PaneConfiguration, splitPane, removePane } from './PaneModel.js';
	import { paneConfiguration } from './PaneStore.js';

	import { createEventDispatcher, onMount } from 'svelte';
	import PaneHandle from './PaneHandle.svelte';

	let dispatch = createEventDispatcher();

	export let draggingStep = 1;

	export let pane: PaneConfiguration;
	export let editMode;
	export let dataStream;
	export let tips;

	let showPercentage: boolean = false;

	function handleUpdate() {
		pane = { ...pane };
		dispatch('update');
	}

	function handleSplit(event: CustomEvent<{ direction: 'horizontal' | 'vertical' }>) {
		splitPane(pane, event.detail.direction);
		handleUpdate();
	}

	function handleDelete(event: CustomEvent) {
		removePane($paneConfiguration, pane);
		handleUpdate();
	}

	function handleResize(child: PaneConfiguration, index: number, size: number) {
		showPercentage = true; // Show percentage while dragging

		// Round size to nearest multiple of draggingStep
		child.size = Math.round(size / draggingStep) * draggingStep;
		if (apis[index]) apis[index].resize(child.size);
		handleUpdate();
	}

	function handleDraggingChange(child: PaneConfiguration) {
		showPercentage = false; // Hide percentage when finished dragging
		handleUpdate();
	}

	onMount(() => {
		showPercentage = false; // Hide percentage on mount
	});

	let apis: Record<number, PaneAPI | undefined> = {};
</script>

{#if pane.split}
	<PaneGroup style={'overflow: hidden'} direction={pane.split}>
		{#each pane.children as child, index}
			<Pane
				defaultSize={child.size}
				style={'overflow: hidden'}
				onResize={(size, _) => {
					handleResize(child, index, size);
				}}
				bind:pane={apis[index]}
			>
				<svelte:self bind:pane={child} {editMode} {dataStream} {tips} on:update={handleUpdate} />
			</Pane>
			{#if editMode}
				{#if pane.children.length > 1 && pane.children.indexOf(child) < pane.children.length - 1}
					<PaneResizer onDraggingChange={() => handleDraggingChange(child)}>
						<PaneHandle direction={pane.split} percentage={child.size} {showPercentage} />
					</PaneResizer>
				{/if}
			{/if}
		{/each}
	</PaneGroup>
{:else}
	{#key pane.split}
		<Tile
			editable={editMode}
			{dataStream}
			bind:item={pane.item}
			{tips}
			on:split={handleSplit}
			on:delete={handleDelete}
			on:update={handleUpdate}
		/>
	{/key}
{/if}
