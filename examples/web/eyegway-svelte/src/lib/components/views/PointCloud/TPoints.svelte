<script lang="ts">
	import type { EyegwayTensor } from '$lib/Eyegway.js';
	import { T } from '@threlte/core';

	export let vertices: EyegwayTensor | null = null;
	export let colors: EyegwayTensor | null = null;
	export let pointSize: number = 0.01;
</script>

<T.Points>
	<T.BufferGeometry>
		{#if vertices != null}
			<T.BufferAttribute
				args={[vertices.data, 3]}
				attach={(parent, self) => {
					parent.setAttribute('position', self);
					return () => {};
				}}
			/>

			{#if colors != null}
				<T.BufferAttribute
					args={[colors.data, 3]}
					attach={(parent, self) => {
						parent.setAttribute('color', self);
						return () => {};
					}}
				/>
			{:else}
				<T.BufferAttribute
					args={[vertices.data, 3]}
					attach={(parent, self) => {
						parent.setAttribute('color', self);
						return () => {};
					}}
				/>
			{/if}
		{/if}
	</T.BufferGeometry>

	<T.PointsMaterial size={pointSize} vertexColors={true} />
</T.Points>
