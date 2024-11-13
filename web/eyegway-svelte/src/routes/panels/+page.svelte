<script lang="ts">
	import HubPanel from '$lib/components/hubs/HubPanel.svelte';
	import Wall from '$lib/components/panels/Wall.svelte';

	let sharedData: any[] = [];
	let editableMosaic: boolean = false;
</script>

<div class="box container mb-1 mt-2 header">
	<div class="columns is-vcentered">
		<div class="column logo-container">
			<img src="images/logo.png" alt="Logo" class="logo" />
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
		--color-background: #ffffff;
		--color-grad-start: #ffffff;
		--color-grad-end: #ebebeb;
		--color-header-buttons: #444444;
	}
	:global(html) {
		background-color: var(--color-background);
		background-image: radial-gradient(
			at center center,
			var(--color-grad-start) 27%,
			var(--color-grad-end) 100%
		);
	}

	.header {
		background-color: var(--color-header);
	}
	.content {
		height: 80vh;
		background-color: var(--color-content);
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
