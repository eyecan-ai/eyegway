<script lang="ts">
	import { GridItem } from 'svelte-grid-extended';
	import type { ProtoypeItem } from './items/DynamicGrid';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let prototype: ProtoypeItem | null = null;
	export let tips: string[] = [];

	function onDelete() {
		console.log('delete', prototype);
		dispatch('delete', prototype);
	}
	$: {
		if (prototype) {
			if (prototype.name.length == 0) onDelete();
		}
	}
</script>

{#if prototype}
	<GridItem
		bind:x={prototype.x}
		bind:y={prototype.y}
		bind:w={prototype.w}
		bind:h={prototype.h}
		activeClass="grid-item-active"
		previewClass="bg-green rounded"
	>
		<div class="item">
			<div>
				<div class="label">Select Data:</div>
				<input class="input is-small" list="tips" bind:value={prototype.name} />
				<datalist id="tips">
					{#each tips as tip}
						<option value={tip} />
					{/each}
				</datalist>
			</div>
			<!-- <button class="button is-small is-danger is-outlined" on:click={onDelete}>deletex</button> -->
		</div>
	</GridItem>
{/if}

<style>
	.item {
		display: grid;
		place-items: center;
		background-color: #fafafa;
		width: 100%;
		height: 100%;
		overflow: hidden;
		padding: 20px;
	}
	.item .input {
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
</style>
