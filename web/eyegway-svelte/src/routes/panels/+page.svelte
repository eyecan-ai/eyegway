<script lang="ts">
	import HubPanel from '$lib/components/hubs/HubPanel.svelte';
	import Wall from '$lib/components/panels/Wall.svelte';
	import { styleSettings } from '$lib/components/panels/settings/StyleSettingsStore.js';

	let sharedData: any[] = [];
	let editableMosaic: boolean = false;
</script>

<div class="box container mb-1 mt-2 header">
	<div class="columns is-vcentered">
		<div class="column logo-container">
			<img
				src={$styleSettings.color.logo ? $styleSettings.color.logo : 'images/logo.png'}
				alt="Logo"
				class="logo"
			/>
		</div>
		<div class="column">
			<HubPanel bind:data={sharedData} />
		</div>
	</div>
</div>

<div class="card container p-0 mt-4 content">
	<Wall dataStream={sharedData} editMode={editableMosaic} />
</div>

<style>
	:root {
		--color-card: #f5f5f5;
		--color-card-empty: #fdfdfd6c;
		--color-header: #ffffff;
		--color-content: #ffffff;
		--color-grad-start: #ffffff;
		--color-grad-end: #ebebeb;
		--color-header-buttons: #444444;
	}
	:global(html) {
		background-image: radial-gradient(
			at center center,
			var(--color-internal-gradient) 27%,
			var(--color-external-gradient) 100%
		);
	}

	.header {
		background-color: var(--color-header);
	}
	.content {
		height: 80vh;
		background-color: var(--color-container);
	}
	.card {
		border-radius: 10px;
	}
	.logo {
		display: flex;
		height: 30px;
		align-items: center;
		padding-left: 25px;
	}
</style>
