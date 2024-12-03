<script lang="ts">
	import HubPanel from '$lib/components/hubs/HubPanel.svelte';
	import Wall from '$lib/components/panels/Wall.svelte';
	import { styleSettings } from '$lib/components/panels/settings/SettingsStore.js';

	let sharedData: any[] = [];
	let editableMosaic: boolean = false;
</script>

<div class="container is-fluid">
	<div class="box mb-1 mt-2 header">
		<div class="columns is-vcentered">
			<div class="column logo-container">
				<img
					src={$styleSettings.eyegway.logo ? $styleSettings.eyegway.logo : 'images/logo.png'}
					alt="Logo"
					class="logo"
				/>
			</div>
			<div class="column">
				<HubPanel bind:data={sharedData} />
			</div>
		</div>
	</div>

	<div class="card p-0 mt-4 content">
		<Wall dataStream={sharedData} editMode={editableMosaic} />
	</div>
</div>

<style>
	:root {
		--color-header: rgba(255, 255, 255, 0);
		--color-content: #ffffff;
		--color-grad-start: #ffffff;
		--color-grad-end: #ebebeb;
		--color-header-buttons: #444444;
	}
	:global(html) {
		background-image: radial-gradient(
			at center center,
			rgba(
					var(--eyegway-background-first-color-r),
					var(--eyegway-background-first-color-g),
					var(--eyegway-background-first-color-b),
					var(--eyegway-background-first-color-a)
				)
				27%,
			rgba(
					var(--eyegway-background-second-color-r),
					var(--eyegway-background-second-color-g),
					var(--eyegway-background-second-color-b),
					var(--eyegway-background-second-color-a)
				)
				100%
		);
		overflow: hidden;
	}
	.header {
		background-color: rgba(
			var(--eyegway-header-background-color-r),
			var(--eyegway-header-background-color-g),
			var(--eyegway-header-background-color-b),
			var(--eyegway-header-background-color-a)
		);
	}
	.content {
		flex-grow: 1;
		height: 100%;
		width: 100%;
		background-color: rgba(
			var(--eyegway-content-background-color-r),
			var(--eyegway-content-background-color-g),
			var(--eyegway-content-background-color-b),
			var(--eyegway-content-background-color-a)
		);
	}
	.container {
		display: flex;
		flex-direction: column;
		height: 100vh;
		padding-bottom: 50px;
	}
	.logo {
		display: flex;
		height: 30px;
		align-items: center;
		padding-left: 25px;
	}
</style>
