<script lang="ts">
	import type { EyegwayTensor } from '$lib/Eyegway.js';

	export let tensor: EyegwayTensor | null = null;
	export let fixed: number = 3;
	let invalidShape: boolean = true;

	let shape: number[] = [];
	let data: number[] = [];

	$: if (tensor) {
		invalidShape = false;
		shape = tensor.shape;
		data = tensor.data;

		if (shape.length == 1) {
			shape = [1, tensor.shape[0]];
		}
		if (shape.length > 3) {
			invalidShape = true;
		}
	}
</script>

{#if tensor}
	{#if invalidShape}
		<div class="notification is-danger">
			Invalid shape: {JSON.stringify(tensor.shape)}
		</div>
	{:else}
		<table class="table p-0 m-0">
			{#each Array.from({ length: shape[0] }) as _, i}
				<tr>
					{#each Array.from({ length: shape[1] }) as _, j}
						<td class="p-2">
							{data[j + i * shape[1]].toFixed(fixed)}
						</td>
					{/each}
				</tr>
			{/each}
		</table>
	{/if}
{/if}
