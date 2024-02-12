<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';

	export let hubName: string = 'fai4ba';
	export let data: any | null = null;
	let historySize: number = -1;
	let bufferSize: number = -1;
	let dataPointer: number = 0;

	export async function reload() {
		const client = new EyegwayHubClient(hubName);
		historySize = await client.historySize();
		bufferSize = await client.bufferSize();
		data = await client.last(dataPointer);
		console.log(data);
	}

	async function increasePointer(delta: number) {
		dataPointer += delta;
		dataPointer = Math.max(0, dataPointer);
		dataPointer = Math.min(historySize - 1, dataPointer);
		await reload();
	}
</script>

<div class="columns is-vcentered">
	<div class="column is-narrow">
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<label>Hub:</label>
	</div>

	<div class="column is-narrow">
		<input class="input is-small" bind:value={hubName} />
	</div>
	<div class="column is-narrow">
		<button class="button is-small is-primary is-outlined" on:click={reload}>Reload</button>
	</div>
	<!-- <div class="column is-narrow">|</div>
	<div class="column is-narrow">
		<div class="field is-grouped is-grouped-multiline">
			<div class="control">
				<div class="tags has-addons">
					<span class="tag is-medium is-info is-light">History</span>
					<span class="tag is-medium is-success is-light">{historySize}</span>
					<span class="tag is-medium is-info is-light">Buffer</span>
					<span class="tag is-medium is-success is-light">{bufferSize}</span>
				</div>
			</div>
			<div class="control">
				<div class="tags has-addons"></div>
			</div>
		</div>
	</div> -->
	{#if data}
		<div class="column is-narrow">|</div>
		<div class="column is-narrow">
			<div class="tags has-addons">
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<span
					class="tag is-medium interactive is-info"
					on:click={() => {
						increasePointer(-1);
					}}
					>{'<'}
				</span>
				<span class="tag is-medium is-primary">{dataPointer + 1} / {historySize}</span>
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<span
					class="tag is-medium interactive is-info"
					on:click={() => {
						increasePointer(1);
					}}
					>{'>'}
				</span>
			</div>
		</div>
	{/if}
</div>

<style>
	.tag.interactive {
		cursor: pointer;
		transition: all 0.1s ease-in-out;
		user-select: none;
	}
	.tag.interactive:hover {
		transform: scale(1.1);
	}
	.tag.interactive:active {
		transform: scale(0.9);
	}
</style>
