<script lang="ts">
	import type { DataImage } from '../MosaicModel.js';

	export let userData: DataImage | null = null;
</script>

{#if userData}
	<div class="image-container" style="background-image: url({userData.url})"></div>
{/if}

<style>
	.image-container {
		border-radius: 10px;
		background-size: contain;
		background-repeat: no-repeat;
		background-position: center;
		width: 100%;
		height: 100%;
	}
</style>
