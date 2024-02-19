<script lang="ts">
	import type { DataImage } from '../MosaicModel.js';

	export let userData: DataImage | null = null;
</script>

{#if userData}
	<img class="item-image" src={userData.url} alt="thumbnail" draggable="false" />
{/if}

<style>
	img {
		width: 100%;
		height: 100%;
		object-fit: contain;
	}
</style>
