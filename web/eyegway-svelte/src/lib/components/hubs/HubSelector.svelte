<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';
	import { HubsPreferences, ServerPreferences } from '$lib/Stores.js';
	import HubSettings from './HubSettings.svelte';
	import { Box } from 'lucide-svelte';

	export let hubName: string | null = null;
	let hubs: string[] = [];
	let isOpen: boolean = false;
	let isError: boolean = false;

	async function toggle() {
		isOpen = !isOpen;
		if (isOpen) await reload();
	}

	async function reload() {
		hubs = [];
		isError = false;
		const client = new EyegwayHubClient('', $ServerPreferences.host);
		try {
			hubs = await client.listHubs($ServerPreferences.hubTriggerKey);
		} catch (e) {
			isError = true;
		}
	}

	$: if (hubName !== null) {
		$HubsPreferences.activeHub = hubName;
	}
</script>

<div class="">
	<div class="dropdown is-right" class:is-active={isOpen}>
		<div class="dropdown-trigger">
			<button class="button is-small is-outlined is-white" on:click={toggle}>
				<span class="mr-2 has-text-weight-bold">
					{#if hubName}
						{hubName}
					{:else}
						<em>Select a hub ...</em>
					{/if}
				</span>
				<Box size={18} strokeWidth={1} />
			</button>
		</div>
		<div class="dropdown-menu" id="dropdown-menu4" role="menu">
			<div class="dropdown-content has-background-dark">
				<div class="dropdown-item">
					{#if hubs.length == 0}
						{#if isError}
							<article class="message is-danger">
								<div class="message-body">Server not connected</div>
							</article>
						{:else}
							<article class="message">
								<div class="message-body">No hubs found</div>
							</article>
						{/if}
					{/if}
					{#each hubs as hub}
						<button
							class="button is-small is-light is-fullwidth"
							class:is-outlined={hubName !== hub}
							on:click={() => {
								hubName = hub;
								isOpen = false;
							}}>{hub}</button
						>
					{/each}
				</div>
				<div class="dropdown-item">
					<HubSettings />
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	.dropdown-trigger .button {
		color: var(--color-header-buttons) !important;
		border-color: var(--color-header-buttons) !important;
	}
	.dropdown-trigger .button:hover {
		color: var(--color-header) !important;
		border-color: var(--color-header) !important;
		background-color: var(--color-header-buttons) !important;
	}
	.dropdown-trigger .button:focus {
		color: var(--color-header) !important;
		border-color: var(--color-header) !important;
		background-color: var(--color-header-buttons) !important;
	}
	.dropdown-content {
		color: var(--color-header) !important;
		background-color: var(--color-header-buttons) !important;
	}
	.dropdown-item .button {
		border-color: var(--color-header) !important;
	}
</style>
