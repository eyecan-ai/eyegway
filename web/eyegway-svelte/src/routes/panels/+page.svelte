<script lang="ts">
	import HubPanel from '$lib/components/hubs/HubPanel.svelte';
	import Wall from '$lib/components/panels/Wall.svelte';
	import { Parameters } from '$lib/Parameters.js';

	let sharedData: any[] = [{ name: 'Tile 1' }, { name: 'Tile 2' }];
	let editableMosaic: boolean = false;
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

<div class="box container p-0 mt-0 wall">
	<Wall dataStream={sharedData} editMode={editableMosaic} />
</div>

<style>
	.logo {
		height: 24px;
	}
	.wall {
		height: 80vh;
	}
</style>
