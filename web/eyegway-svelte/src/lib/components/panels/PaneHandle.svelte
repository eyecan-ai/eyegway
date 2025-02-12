<script lang="ts">
	import { GripHorizontal, GripVertical } from 'lucide-svelte';

	export let direction: string;
	export let percentage: number = 0;
	export let showPercentage: boolean = false;
</script>

{#if direction == 'vertical'}
	<div
		class="is-flex is-flex-direction-column is-align-items-center is-justify-content-center dots vertical"
	>
		<span class="percent">{showPercentage ? percentage + '%' : ''}</span>
		<div class="is-flex vertical">
			<GripHorizontal
				size={20}
				style="color: var(--bulma-scheme-main); background-color: var(--bulma-text-strong); border-radius: 4px;  z-index: 10; border: 2px solid var(--bulma-text);"
			/>
		</div>
		<span class="percent">{showPercentage ? 100 - percentage + '%' : ''}</span>
	</div>
{:else}
	<div
		class=" is-flex is-flex-direction-row is-align-items-center is-justify-content-center dots horizontal"
	>
		<div class="is-flex horizontal">
			<span class="percent">{showPercentage ? percentage + '%' : ''}</span>
			<GripVertical
				size={20}
				style="color: var(--bulma-scheme-main); background-color: var(--bulma-text-strong); border-radius: 4px;  z-index: 10; border: 2px solid var(--bulma-text);"
			/>
			<span class="percent">{showPercentage ? 100 - percentage + '%' : ''}</span>
		</div>
	</div>
{/if}

<style>
	.dots {
		color: var(--bulma-scheme-main);
		width: 100%;
		height: 100%;
	}
	.dots.vertical {
		height: 2px;
		background: linear-gradient(
			to right,
			#ffffff00 0%,
			#ffffff00 14%,
			var(--bulma-border) 15%,
			var(--bulma-border) 85%,
			#ffffff00 86%,
			#ffffff00 100%
		);
	}
	.dots.horizontal {
		width: 2px;
		background: linear-gradient(
			to bottom,
			#ffffff00 0%,
			#ffffff00 14%,
			var(--bulma-border) 15%,
			var(--bulma-border) 85%,
			#ffffff00 86%,
			#ffffff00 100%
		);
	}
	.percent {
		color: var(--bulma-text);
		font-size: 0.7em;
		font-weight: bold;
		padding-left: 5px;
		padding-right: 5px;
		z-index: 10;
		mix-blend-mode: exclusion;
		filter: invert();
	}
</style>
