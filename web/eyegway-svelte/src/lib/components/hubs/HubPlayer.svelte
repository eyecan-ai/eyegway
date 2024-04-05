<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';
	import { ServerPreferences } from '$lib/Stores.js';
	import {
		IconChevronLeft,
		IconChevronRight,
		IconReload,
		IconSettings,
		IconPlayerPlay,
		IconPlayerStop,
		IconIceCream,
		IconDotsVertical
	} from '@tabler/icons-svelte';
	import { onDestroy } from 'svelte';

	export let hubName: string | null = null;
	export let data: any | null = null;
	let hubClient: EyegwayHubClient | null = null;
	let historyFrozen: boolean = false;
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
			historyFrozen = await hubClient.isHistoryFrozen();
			if (historyFrozen) {
				autoPlay = false;
			}
		} catch (e) {
			console.log(e);
		}
	}

	export async function reload() {
		if (hubClient === null) return;
		try {
			historySize = await hubClient.historySize();
			bufferSize = await hubClient.bufferSize();
			historyFrozen = await hubClient.isHistoryFrozen();
			data = await hubClient.last(dataPointer);
		} catch (e) {
			console.log(e);
			data = null;
		}
		console.log('Reloading ...');
	}

	export async function reloadData() {
		if (hubClient === null) return;
		try {
			console.log('reloadin datapointer', dataPointer);
			data = await hubClient.last(dataPointer);
		} catch (e) {
			console.log(e);
			data = null;
		}
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

	async function toggleFreeze() {
		if (hubClient === null) return;
		try {
			if (historyFrozen) await hubClient.unfreezeHistory();
			else await hubClient.freezeHistory();

			dataPointer = 0;
			await reloadInfo();
			await reloadData();
		} catch (e) {
			console.log(e);
		}
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

<div class="columns is-vcentered is-variable is-0">
	{#if hubClient}
		{#if historyFrozen}
			<div class="column is-narrow">
				<div class="field has-addons">
					<!----------------------------->
					<!-- History offset controls -->
					<!----------------------------->
					<p class="control">
						<button
							class="button is-small p-0"
							on:click={() => setDataPointer(-1)}
							disabled={!historyFrozen || dataPointer == 0}
						>
							<IconChevronLeft size={24} />
						</button>
					</p>
					<p class="control">
						<button
							class="button is-small p-2"
							on:click={() => setDataPointer(null)}
							disabled={!historyFrozen}
						>
							{dataPointer + 1} / {historySize}
						</button>
					</p>
					<p class="control">
						<button
							class="button is-small p-0"
							on:click={() => setDataPointer(1)}
							disabled={!historyFrozen || dataPointer == historySize - 1}
						>
							<IconChevronRight size={24} />
						</button>
					</p>
				</div>
			</div>
		{:else}
			<!------------------->
			<!-- Play controls -->
			<!------------------->
			<div class="column">
				<!--------------------->
				<!-- Play settings -->
				<!--------------------->
				<div class="field has-addons">
					<div class="dropdown is-right" class:is-hoverable={!historyFrozen}>
						<div class="dropdown-trigger">
							<button class="button is-small" disabled={historyFrozen}>
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
					<!--------------------->
					<!-- Reload current -->
					<!--------------------->
					<p class="control">
						<button
							class="button is-small"
							on:click={reload}
							disabled={historyFrozen}
							title="Click to trigger a single update"
						>
							<IconReload stroke={1} />
						</button>
					</p>

					<!--------------------->
					<!-- Play  -->
					<!--------------------->
					<p class="control">
						<button
							class="button is-small is-outlined"
							style="--animation-time: {autoPlayMs}ms;"
							class:blink={autoPlay}
							disabled={historyFrozen}
							on:click={() => {
								autoPlay = !autoPlay;
							}}
							title="Click to auto update every {autoPlayMs}ms"
						>
							{#if !autoPlay}
								<IconPlayerPlay stroke={1} />
							{:else}
								<IconPlayerStop stroke={1} />
							{/if}
						</button>
					</p>
				</div>
			</div>
		{/if}

		<div class="column is-narrow is-flex">
			<IconDotsVertical stroke={1} />
		</div>
		<div class="column">
			<button
				class="button is-small is-outlined"
				style="--animation-time: {autoPlayMs}ms;"
				class:is-info={historyFrozen}
				class:is-primary={!historyFrozen}
				on:click={toggleFreeze}
				title={!historyFrozen ? 'Click to freeze History' : 'Click to unfreeze History'}
			>
				{#if historyFrozen}
					Frozen
				{:else}
					Running
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
