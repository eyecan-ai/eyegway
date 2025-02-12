<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';
	import { ServerPreferences } from '$lib/Stores.js';
	import { Slider, Stepper, Pane } from 'svelte-tweakpane-ui';

	import { CirclePlay, CircleStop, Settings, RotateCw, EllipsisVertical } from 'lucide-svelte';
	import { onDestroy } from 'svelte';

	export let hubName: string | null = null;
	export let data: any | null = null;
	export let iconSize: number = 18;
	let hubClient: EyegwayHubClient | null = null;
	let historyFrozen: boolean = false;
	let historySize: number = -1;
	let bufferSize: number = -1;
	let dataPointer: number = 0;
	let autoPlay: boolean = true;
	let autoPlayMs: number = 500;
	let sliderDebounce: number = 5;
	let sliderTimeout: number | null = null;
	let autoPlayTimeout: number | null = null;
	let settingsOpen: boolean = false;

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
			data = await hubClient.last(-dataPointer);
		} catch (e) {
			console.log(e);
			data = null;
		}
	}

	// Debounced reload function for slider changes
	function debouncedReload() {
		if (sliderTimeout !== null) clearTimeout(sliderTimeout);
		sliderTimeout = setTimeout(() => {
			reload();
		}, sliderDebounce);
	}

	export async function reloadData() {
		if (hubClient === null) return;
		try {
			console.log('reloadin datapointer', dataPointer);
			data = await hubClient.last(-dataPointer);
		} catch (e) {
			console.log(e);
			data = null;
		}
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

<div class="columns is-vcentered is-variable is-0 is-mobile">
	{#if hubClient}
		{#if historyFrozen}
			<button class="button is-small p-0">
				<Pane
					position={'inline'}
					width={125}
					theme={{
						baseShadowColor: 'rgba(0, 0, 0, 0)',
						baseBackgroundColor: 'transparent'
					}}
				>
					<Slider
						bind:value={dataPointer}
						max={0}
						min={-(historySize - 1)}
						step={1}
						on:change={debouncedReload}
						format={(value) => {
							return `${value}`;
						}}
					/>
				</Pane>
			</button>
		{:else}
			<!------------------->
			<!-- Play controls -->
			<!------------------->
			<div class="column">
				<!--------------------->
				<!-- Play settings -->
				<!--------------------->
				<div class="field has-addons">
					<div class="dropdown is-right {settingsOpen ? 'is-active' : ''}">
						<div class="dropdown-trigger">
							<button
								class="button is-small"
								class:is-inverted={settingsOpen}
								disabled={historyFrozen}
								on:click={() => {
									settingsOpen = !settingsOpen;
								}}
							>
								<Settings strokeWidth={2} size={iconSize} />
							</button>
						</div>
						<div class="dropdown-menu" id="dropdown-menu4" role="menu">
							<div class="dropdown-content settings">
								<div class="dropdown-item">
									<div class="field">
										<!-- svelte-ignore a11y-label-has-associated-control -->
										<div class="control">
											<Stepper bind:value={autoPlayMs} label="Auto Play Delay (ms)" step={10} />
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
							<RotateCw strokeWidth={2} size={iconSize} />
						</button>
					</p>

					<!--------------------->
					<!-- Play  -->
					<!--------------------->
					<p class="control">
						<button
							class="button is-small"
							style="--animation-time: {autoPlayMs}ms;"
							class:blink={autoPlay}
							disabled={historyFrozen}
							on:click={() => {
								autoPlay = !autoPlay;
							}}
							title="Click to auto update every {autoPlayMs}ms"
						>
							{#if !autoPlay}
								<CirclePlay strokeWidth={2} size={iconSize} />
							{:else}
								<CircleStop strokeWidth={2} size={iconSize} />
							{/if}
						</button>
					</p>
				</div>
			</div>
		{/if}

		<div class="column is-narrow is-flex">
			<EllipsisVertical strokeWidth={0.5} />
		</div>
		<div class="column">
			<button
				class="button is-small has-text-weight-semibold is-outlined"
				style="--animation-time: {autoPlayMs}ms;"
				class:is-info={historyFrozen}
				class:is-primary={!historyFrozen}
				on:click={toggleFreeze}
				title={!historyFrozen ? 'Click to freeze History' : 'Click to unfreeze History'}
			>
				{#if historyFrozen}
					<p class="is-hidden-tablet">F</p>
					<p class="is-hidden-mobile play-button">Frozen</p>
				{:else}
					<p class="is-hidden-tablet">R</p>
					<p class="is-hidden-mobile play-button">Running</p>
				{/if}
			</button>
		</div>
	{/if}
</div>

<style>
	.play-button {
		width: 45px;
	}
	.settings {
		width: 350px;
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
