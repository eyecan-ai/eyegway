<script lang="ts">
	import { EyegwayHubClient } from '$lib/Eyegway.js';
	import { HubsPreferences, ServerPreferences } from '$lib/Stores.js';
	import { DataExtractor } from '$lib/components/mosaic/MosaicModel.js';
	import ViewGeneric from '$lib/components/mosaic/views/ViewGeneric.svelte';
	let hubName: string = $HubsPreferences.activeHub ? $HubsPreferences.activeHub : '';
	let itemName: string = '';
	let historyOffset: number = 0;
	let wholeData: any | null = null;
	let extractedData: any | null = null;
	let errorMessage: string | null = null;

	async function clear() {
		hubName = $HubsPreferences.activeHub ? $HubsPreferences.activeHub : '';
		itemName = '';
		historyOffset = 0;
		wholeData = null;
		extractedData = null;
		errorMessage = null;
	}

	async function update() {
		errorMessage = null;
		wholeData = null;
		extractedData = null;
		try {
			const hub = new EyegwayHubClient(hubName, $ServerPreferences.host);
			wholeData = await hub.last(historyOffset);
		} catch (e) {
			console.log(e);
			errorMessage = e.message;
		}
		if (itemName.length > 0) {
			extractedData = DataExtractor.pickAndParse(wholeData, itemName);
		}
		console.log(wholeData);
	}

	$: if (itemName !== undefined) {
		update();
	}

	$: if (historyOffset !== undefined) {
		update();
	}
</script>

<div class="container box mt-2">
	<div class="title is-4">Developers Tools</div>
	<div class="title is-6"><em>Debug Hub data</em></div>
	<div class="field">
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<label class="label">Host:</label>
		<div class="control">
			<input
				class="input"
				type="text"
				placeholder="Hub Rest API Host"
				bind:value={$ServerPreferences.host}
			/>
		</div>
	</div>
	<div class="field">
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<label class="label">Hub Name:</label>
		<div class="control">
			<input class="input" type="text" placeholder="Hub Name" bind:value={hubName} />
		</div>
	</div>

	<div class="field">
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<label class="label">Item Name:</label>
		<div class="control">
			<input
				class="input"
				type="text"
				placeholder="Item name. Leave empty for all items."
				bind:value={itemName}
			/>
		</div>
	</div>

	<div class="field">
		<!-- svelte-ignore a11y-label-has-associated-control -->
		<label class="label">History Offset:</label>
		<div class="control">
			<input class="input" type="number" placeholder="Text input" bind:value={historyOffset} />
		</div>
	</div>
	<div class="field">
		<button class="button" on:click={update}>Test</button>
		<button class="button is-danger is-outlined" on:click={clear}>Clear</button>
	</div>
	{#if errorMessage}
		<div class="notification is-danger">{errorMessage}</div>
	{/if}
</div>

<div class="container box mt-2">
	<div class="columns">
		<div class="column is-4">
			{#if wholeData}
				<!-- iterate wholeData object printing key: typeof value -->
				{#each Object.entries(wholeData) as [key, value]}
					<!-- svelte-ignore a11y-click-events-have-key-events -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<button
						class="button is-fullwidth"
						class:is-info={key === itemName}
						on:click={() => {
							itemName = key;
						}}>{key}<b>|{value?.constructor.name}</b></button
					>
				{/each}
			{/if}
		</div>
		<div class="column is-8">
			{#if extractedData}
				<ViewGeneric userData={extractedData} />
			{/if}
		</div>
	</div>
</div>
