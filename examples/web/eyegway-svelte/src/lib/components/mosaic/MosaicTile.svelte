<script lang="ts">
	import { GridItem } from 'svelte-grid-extended';
	import { createEventDispatcher } from 'svelte';
	import { DataExtractor, type MosaicItem } from './MosaicModel.js';
	import ViewGeneric from './views/ViewGeneric.svelte';

	const dispatch = createEventDispatcher();

	export let item: MosaicItem | null = null;
	export let dataStream: any | null = null;
	export let editable: boolean = false;
	export let tips: string[] = [];

	//
	let extractedData: any | null = null;

	function onDelete() {
		dispatch('delete', item);
	}

	$: if (item) {
		// Extract data picking a key from the data stream
		extractedData = DataExtractor.pickAndParse(dataStream, item.name);
	}
</script>

{#if item}
	{#if editable}
		<!-- ############ -->
		<!-- Editable Mode-->
		<!-- ############ -->
		<GridItem
			bind:x={item.x}
			bind:y={item.y}
			bind:w={item.w}
			bind:h={item.h}
			activeClass="grid-item-active"
			previewClass="bg-green rounded"
		>
			<div slot="moveHandle" class="move-handle" let:moveStart>
				<div
					class="p-2 bg-slate-600 rounded text-white cursor-move"
					on:pointerdown={moveStart}
				></div>
			</div>
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<span class="delete-handle" on:click={onDelete}>x</span>

			<div class="item-editable">
				<div>
					<div class="label">Select data <b>Name</b>:</div>
					<input class="input is-small" list="tips" bind:value={item.name} />
					<datalist id="tips">
						{#each tips as tip}
							<option value={tip} />
						{/each}
					</datalist>
				</div>
			</div>
		</GridItem>
	{:else}
		<!-- ############ -->
		<!-- Play Mode    -->
		<!-- ############ -->
		<GridItem
			x={item.x}
			y={item.y}
			w={item.w}
			h={item.h}
			class="item"
			activeClass=""
			previewClass=""
		>
			<div class="item">
				<ViewGeneric userData={extractedData} />
				<div class="banner">
					{item.name}
				</div>
			</div>
		</GridItem>
	{/if}
{/if}

<style>
	.move-handle {
		position: absolute;
		left: 0;
		width: 100%;
		background-color: #42a5f5;
		height: 24px;
	}
	.delete-handle {
		position: absolute;
		right: 10px;
		cursor: pointer;
		color: #fafafa;
	}
	.delete-handle:hover {
		transform: scale(1.2);
	}
	.item-editable {
		display: grid;
		place-items: center;
		background-color: #bbdefb;
		width: 100%;
		height: 100%;
		overflow: hidden;
		padding: 20px;
	}
	.item-editable .input {
		background-color: #222;
		color: #fafafa;
		border-radius: 10px;
	}
	:global(.grid-item-active) {
		opacity: 0.4;
		z-index: 2 !important;
	}

	:global(.bg-green) {
		background-color: rgb(33, 202, 33);
		position: fixed;
		z-index: 1 !important;
	}
	:global(.rounded) {
		border-radius: 0.25rem;
	}

	.item {
		display: grid;
		/* place-items: stretch; */
		background-color: #222;
		width: 100%;
		height: 100%;
		overflow: scroll;
	}

	.item .banner {
		position: absolute;
		bottom: 0;
		left: 0;
		color: #222;
		background-color: #fafafa;

		padding: 3px;
		opacity: 0.3;
		width: 100%;
		font-size: 0.8em;
		transition: all 0.3s;
	}
	.item:hover .banner {
		opacity: 1;
		transform: scale(1.01);
		box-shadow: 0px 0px 15px #ddd;
	}
</style>
