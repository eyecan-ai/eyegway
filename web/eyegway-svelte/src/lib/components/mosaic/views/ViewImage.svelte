<script lang="ts">
	import type { DataImage } from '../MosaicModel.js';

	export let userData: DataImage | null = null;
</script>

{#if userData}
	<div class="image-container" style="background-image: url({userData.url})"></div>
{/if}

<style>
	.image-container {
		background-size: contain;
		background-repeat: no-repeat;
		background-position: center;
	}
</style>
