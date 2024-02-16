<script lang="ts">
	import type { DataTensor } from '../MosaicModel.js';

	export let userData: DataTensor | null = null;
	export let fixed: number = 3;
	let invalidShape: boolean = true;

	let shape: number[] = [];
	let elements: number[] = [];

	$: if (userData) {
		invalidShape = false;
		shape = userData.tensor.shape;
		elements = userData.tensor.data;

		if (shape.length == 1) {
			shape = [1, userData.tensor.shape[0]];
		}
		if (shape.length > 3) {
			invalidShape = true;
		}
	}
</script>

{#if userData}
	{#if invalidShape}
		<div class="notification is-danger">
			Invalid shape: {JSON.stringify(userData.tensor.shape)}
		</div>
	{:else}
		<table class="table p-0 m-0">
			{#each Array.from({ length: shape[0] }) as _, i}
				<tr>
					{#each Array.from({ length: shape[1] }) as _, j}
						<td class="p-2">
							{elements[j + i * shape[1]].toFixed(fixed)}
						</td>
					{/each}
				</tr>
			{/each}
		</table>
	{/if}
{/if}
