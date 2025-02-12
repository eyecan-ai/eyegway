<script lang="ts">
	import type { DataImage } from '../PaneModel.js';
	import type { ImageSettings } from '../settings/SettingsModel.js';

	export let userData: DataImage | null = null;
	export let userSettings: ImageSettings | null = null;
</script>

{#if userData && userSettings}
	<div
		class="image-container"
		style="background-image: url({userData.url}); background-size: {userSettings.fit};"
	></div>
{/if}

<style>
	.image-container {
		border-radius: 10px;
		background-repeat: no-repeat;
		background-position: center;
		width: 100%;
		height: 100%;
	}
</style>
