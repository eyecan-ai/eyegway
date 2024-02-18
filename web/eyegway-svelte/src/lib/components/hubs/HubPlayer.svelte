<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';
	import { ServerPreferences } from '$lib/Stores.js';
	import {
		IconChevronLeft,
		IconChevronRight,
		IconReload,
		IconSettings,
		IconPlayerPlay,
		IconPlayerStop
	} from '@tabler/icons-svelte';
	import { onDestroy } from 'svelte';

	export let hubName: string | null = null;
	export let data: any | null = null;
	let hubClient: EyegwayHubClient | null = null;
	let historySize: number = -1;
	let bufferSize: number = -1;
	let dataPointer: number = 0;
	let autoPlay: boolean = false;
	let autoPlayMs: number = 500;
	let autoPlayTimeout: number | null = null;

	export async function reloadInfo() {
		if (hubClient === null) return;
		try {
			historySize = await hubClient.historySize();
			bufferSize = await hubClient.bufferSize();
		} catch (e) {
			console.log(e);
		}
	}

	export async function reload() {
		if (hubClient === null) return;
		try {
			historySize = await hubClient.historySize();
			bufferSize = await hubClient.bufferSize();
			data = await hubClient.last(dataPointer);
		} catch (e) {
			console.log(e);
			data = null;
		}
		console.log('Reloading ...');
	}

	async function setDataPointer(delta: number | null) {
		if (delta === null) {
			dataPointer = 0;
		} else {
			dataPointer += delta;
			dataPointer = Math.max(0, dataPointer);
			dataPointer = Math.min(historySize - 1, dataPointer);
		}
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

	// On hubName change
	$: if (hubName !== null) {
		hubClient = new EyegwayHubClient(hubName, $ServerPreferences.host);
	}

	// On hubClient change
	$: if (hubClient !== null) {
		reloadInfo();
		reload();
	}

	// Auto Play Management
	$: if (autoPlay === true) {
		play();
	}

	$: if (autoPlay === false) {
		if (autoPlayTimeout !== null) clearTimeout(autoPlayTimeout);
	}
</script>

<div class="columns is-vcentered is-variable is-1">
	{#if hubClient}
		<div class="column is-narrow">
			<div class="field has-addons">
				<!----------------------------->
				<!-- History offset controls -->
				<!----------------------------->
				<p class="control">
					<button
						class="button p-0"
						on:click={() => setDataPointer(-1)}
						disabled={autoPlay || dataPointer == 0}
					>
						<IconChevronLeft size={24} />
					</button>
				</p>
				<p class="control">
					<button class="button p-2" on:click={() => setDataPointer(null)} disabled={autoPlay}>
						{dataPointer + 1} / {historySize}
					</button>
				</p>
				<p class="control">
					<button
						class="button p-0"
						on:click={() => setDataPointer(1)}
						disabled={autoPlay || dataPointer == historySize - 1}
					>
						<IconChevronRight size={24} />
					</button>
				</p>

				<!--------------------->
				<!-- Reload controls -->
				<!--------------------->
				<p class="control">
					<button class="button" on:click={reload} disabled={autoPlay}>
						<IconReload stroke={1} />
					</button>
				</p>
			</div>
		</div>

		<!------------------------>
		<!-- Settings -->
		<!------------------------>
		<div class="column">
			<div class="dropdown is-right" class:is-hoverable={!autoPlay}>
				<div class="dropdown-trigger">
					<button class="button" disabled={autoPlay}>
						<IconSettings stroke={1} />
					</button>
				</div>
				<div class="dropdown-menu" id="dropdown-menu4" role="menu">
					<div class="dropdown-content settings">
						<div class="dropdown-item">
							<div class="field">
								<!-- svelte-ignore a11y-label-has-associated-control -->
								<label class="label">Auto Play Delay (ms):</label>
								<div class="control">
									<input class="input" type="number" bind:value={autoPlayMs} />
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!------------------->
		<!-- Play controls -->
		<!------------------->
		<div class="column">
			<button
				class="button is-outlined"
				style="--animation-time: {autoPlayMs}ms;"
				class:blink={autoPlay}
				on:click={() => {
					autoPlay = !autoPlay;
				}}
			>
				{#if !autoPlay}
					<IconPlayerPlay stroke={1} />
				{:else}
					<IconPlayerStop stroke={1} />
				{/if}
			</button>
		</div>
	{/if}
</div>

<style>
	.button[disabled] {
		opacity: 0.2;
	}
	.settings {
		width: 300px;
	}

	.blink {
		animation: blink var(--animation-time) infinite;
	}

	@keyframes blink {
		0% {
			transform: scale(0.9);
		}
	}
</style>
