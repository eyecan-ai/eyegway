<script lang="ts">
	import { EllipsisVertical, Download, Upload, Trash } from 'lucide-svelte';

	export let saveConfigurationToFile: () => void;
	export let loadConfigurationFromFile: () => void;
	export let configurationReset: () => void;
</script>

<div class="column is-narrow">
	<EllipsisVertical size={16} />
</div>
<div class="column is-narrow">
	<!-- SAVE TO FILE-->
	<button
		class="button is-small is-info is-inverted"
		on:click={saveConfigurationToFile}
		title="Download current Configuration to File"
	>
		<Download strokeWidth={1} size={18} />
	</button>

	<!-- LOAD FROM FILE-->
	<button
		class="button is-small is-inverted is-info"
		on:click={loadConfigurationFromFile}
		title="Load Configuration from File"
	>
		<Upload strokeWidth={1} size={18} />
	</button>

	<!-- CLEAR LAYOUT -->
	<button
		class="button is-small is-danger is-inverted"
		on:click={configurationReset}
		title="Clear Layout"
	>
		<Trash strokeWidth={1} size={18} />
	</button>
</div>
