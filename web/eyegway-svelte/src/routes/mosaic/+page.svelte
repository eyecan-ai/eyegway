<script lang="ts">
	import HubPanel from '$lib/components/hubs/_HubPanel.svelte';
	import Mosaic from '$lib/components/mosaic/Mosaic.svelte';
	import { Parameters } from '$lib/Parameters.js';

	let sharedData: any | null = null;
	let editableMosaic: boolean = false;
	let mosaic: Mosaic;
</script>

<div class="box container mb-1 mt-2">
	<div class="columns is-vcentered">
		<div class="column is-3">
			<div class="columns is-vcentered">
				<div class="column is-narrow">
					<span class="title is-6">
						{Parameters.title}
					</span>
				</div>
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<!-- svelte-ignore a11y-no-static-element-interactions -->
				<div class="column is-narrow logo-container">
					<img src="images/logo.png" alt="Logo" class="logo" />
				</div>
			</div>
		</div>
		<div class="column is-9">
			<HubPanel bind:data={sharedData} />
		</div>
	</div>
</div>

<div class="box container p-0 mt-0">
	<Mosaic bind:this={mosaic} data={sharedData} editableMode={editableMosaic} />
</div>

<style>
	.logo {
		height: 24px;
	}
</style>
