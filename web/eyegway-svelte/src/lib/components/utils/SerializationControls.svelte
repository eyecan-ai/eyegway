<script lang="ts">
	import { slide, fade } from 'svelte/transition';
	import { EllipsisVertical, Download, Upload, Trash, RefreshCcwDot } from 'lucide-svelte';

	export let saveConfigurationToFile: () => void;
	export let loadConfigurationFromFile: () => void;
	export let configurationReset: () => void;
</script>

<div transition:slide={{ axis: 'x' }} class="columns is-vcentered is-variable is-1">
	<div class="column is-narrow">
		<EllipsisVertical size={16} />
	</div>
	<div class="column is-narrow">
		<!-- SAVE TO FILE-->
		<button
			class="button is-small is-info is-outlined"
			on:click={saveConfigurationToFile}
			title="Save Configuration to File"
		>
			<Download strokeWidth={2} size={16} />
		</button>
	</div>
	<div class="column is-narrow">
		<!-- LOAD FROM FILE-->
		<button
			class="button is-small is-info is-outlined"
			on:click={loadConfigurationFromFile}
			title="Load Configuration from File"
		>
			<Upload strokeWidth={2} size={16} />
		</button>
	</div>
	<div class="column is-narrow">
		<!-- CLEAR LAYOUT -->
		<button
			class="button is-small is-danger is-outlined"
			on:click={() => {
				configurationReset();
				console.log('Clear Layout');
			}}
			title="Reset to Default"
		>
			<RefreshCcwDot strokeWidth={2} size={16} />
		</button>
	</div>
</div>
