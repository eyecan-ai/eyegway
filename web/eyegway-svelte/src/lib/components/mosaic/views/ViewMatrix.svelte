<script lang="ts">
	import type { DataTensor } from '../MosaicModel.js';

	export let userData: DataTensor | null = null;
	export let fixed: number = 3;
	export let maxElements: number = 64;
	let invalidData: boolean = true;

	let shape: number[] = [];
	let elements: number[] = [];

	/**
	 * Parse value to fixed number of decimals. Manage also BigInts and evantual errors
	 * @param number
	 */
	function parsedValue(number: any) {
		try {
			const value = parseFloat(number);
			return value.toFixed(fixed);
		} catch (e) {
			console.error('Error parsing value in ViewMatrix', e);
			return 'NaN';
		}
	}

	$: if (userData) {
		invalidData = false;
		shape = userData.tensor.shape;
		elements = userData.tensor.data;

		if (shape.length == 1) {
			shape = [1, userData.tensor.shape[0]];
		}
		if (shape.length > 2) {
			invalidData = true;
		}

		if (!invalidData) {
			if (elements.length > maxElements) {
				invalidData = true;
			}
		}
	}
</script>

{#if userData}
	{#if invalidData}
		<div class="notification is-danger">
			Cannot show Tensor with shape: {JSON.stringify(userData.tensor.shape)}
			Or too many elements: {userData.tensor.data.length} [Max:{maxElements}]
		</div>
	{:else}
		<table class="table p-0 m-0">
			{#each Array.from({ length: shape[0] }) as _, i}
				<tr>
					{#each Array.from({ length: shape[1] }) as _, j}
						<td class="p-2">
							{parsedValue(elements[j + i * shape[1]])}
						</td>
					{/each}
				</tr>
			{/each}
		</table>
	{/if}
{/if}
