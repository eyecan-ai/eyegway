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
			hubs = await client.listHubs();
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
			<button class="button is-small" on:click={toggle}>
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
			<div class="dropdown-content">
				<div class="dropdown-item has-text-weight-bold">
					{#if hubs.length == 0}
						{#if isError}
							<div class="dropdown-item has-text-weight-bold has-text-danger">
								Server not connected
							</div>
						{:else}
							<div class="dropdown-item has-text-weight-bold has-text-warning">No hubs found</div>
						{/if}
					{/if}
				</div>
				{#each hubs as hub}
					<a
						href={'#'}
						class="dropdown-item has-text-weight-bold"
						class:is-active={hub == hubName}
						on:click={() => {
							hubName = hub;
							isOpen = false;
						}}>{hub}</a
					>
				{/each}
				<div class="dropdown-item">
					<HubSettings />
				</div>
			</div>
		</div>
	</div>
</div>

<style>
</style>
