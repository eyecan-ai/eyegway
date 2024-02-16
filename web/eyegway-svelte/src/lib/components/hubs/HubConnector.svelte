<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';
	import { onDestroy } from 'svelte';

	export let hubName: string = 'fai4ba';
	export let data: any | null = null;
	let historySize: number = -1;
	let bufferSize: number = -1;
	let dataPointer: number = 0;
	let autoPlay: boolean = false;
	let autoPlayMs: number = 1000;
	let autoPlayTimeout: number | null = null;

	export async function reload() {
		const client = new EyegwayHubClient(hubName);
		historySize = await client.historySize();
		bufferSize = await client.bufferSize();
		data = await client.last(dataPointer);
		console.log('Reloading ...');
	}

	async function increasePointer(delta: number) {
		dataPointer += delta;
		dataPointer = Math.max(0, dataPointer);
		dataPointer = Math.min(historySize - 1, dataPointer);
		await reload();
	}

	async function play() {
		dataPointer = 0;
		autoPlayTimeout = setInterval(async () => {
			await reload();
		}, autoPlayMs);
	}

	onDestroy(() => {
		if (autoPlayTimeout !== null) clearTimeout(autoPlayTimeout);
	});

	// Auto Play Management
	$: if (autoPlay === true) {
		play();
	}

	$: if (autoPlay === false) {
		if (autoPlayTimeout !== null) clearTimeout(autoPlayTimeout);
	}
</script>

<div class="columns is-vcentered">
	<div class="column is-narrow">
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<div class="tags has-addons">
			<span class="tag is-medium is-info is-light">Hub:</span>
			<span class="tag is-medium"><input class="input" bind:value={hubName} /></span>
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-static-element-interactions -->
			<span class="tag is-medium interactive is-primary is-light" on:click={reload}>Reload</span>
		</div>
	</div>

	{#if data}
		<div class="column is-narrow">|</div>
		<div class="column is-narrow">
			<div class="tags has-addons">
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<span
					style="--animation-time: {autoPlayMs}ms;"
					class="tag is-medium interactive is-primary is-light"
					class:blink={autoPlay}
					on:click={() => {
						autoPlay = !autoPlay;
					}}
				>
					{autoPlay ? 'Stop' : 'Auto Play'}
				</span>
				{#if !autoPlay}
					<span class="tag is-medium"
						><input class="input" type="number" bind:value={autoPlayMs} /> ms</span
					>
				{/if}
			</div>
		</div>
		{#if !autoPlay}
			<div class="column is-narrow">|</div>
			<div class="column is-narrow">
				<div class="tags has-addons">
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<span
						class="tag is-medium interactive is-primary is-light"
						on:click={() => {
							increasePointer(-1);
						}}
						>{'<'}
					</span>
					<span class="tag is-medium is-info is-light">{dataPointer + 1} / {historySize}</span>
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<span
						class="tag is-medium interactive is-primary is-light"
						on:click={() => {
							increasePointer(1);
						}}
						>{'>'}
					</span>
				</div>
			</div>
		{/if}
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
	.tags input {
		border: none;
		box-shadow: none;
		background: none;
		padding: 0px;
		height: 100%;
	}
	.tags input:focus {
		border: none;
		border-bottom: 1px dashed #222;
		border-radius: 0px;
	}
	.blink {
		animation: blink var(--animation-time) infinite;
	}

	@keyframes blink {
		0% {
			/* transform: scale(1.1); */
			color: red;
		}
	}
</style>
