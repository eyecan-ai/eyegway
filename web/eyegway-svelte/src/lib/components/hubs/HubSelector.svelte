<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';
	import { IconCube } from '@tabler/icons-svelte';

	export let hubName: string | null = null;
	let hubs: string[] = [];
	let isOpen: boolean = false;

	async function toggle() {
		isOpen = !isOpen;
		if (isOpen) await reload();
	}

	async function reload() {
		const client = new EyegwayHubClient('');
		hubs = await client.listHubs();
	}
</script>

<div class="">
	<div class="dropdown" class:is-active={isOpen}>
		<div class="dropdown-trigger">
			<button class="button" on:click={toggle}>
				<span class="mr-2">
					{#if hubName}
						{hubName}
					{:else}
						<em>Select a hub ...</em>
					{/if}
				</span>
				<IconCube size={24} stroke={1} />
			</button>
		</div>
		<div class="dropdown-menu" id="dropdown-menu4" role="menu">
			<div class="dropdown-content">
				<div class="dropdown-item">
					{#each hubs as hub}
						<button
							class="button is-small is-outlined is-dark is-fullwidth"
							on:click={() => {
								hubName = hub;
								isOpen = false;
							}}>{hub}</button
						>
					{/each}
				</div>
			</div>
		</div>
	</div>
</div>

<style>
</style>
