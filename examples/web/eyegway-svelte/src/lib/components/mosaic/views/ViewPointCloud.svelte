<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { Grid, OrbitControls } from '@threlte/extras';
	import type { DataPointCloud } from '../MosaicModel.js';

	export let userData: DataPointCloud | null = null;
	export let pointSize: number = 0.01;
	export let width: number = 100;
	export let height: number = 100;
	let maxDistance = 1;
	let container: HTMLElement;

	$: {
		if (container && container.parentElement) {
			if (ResizeObserver) {
				const observer = new ResizeObserver((entries) => {
					for (let entry of entries) {
						width = entry.contentRect.width;
						height = entry.contentRect.height;
					}
				});
				observer.observe(container.parentElement);
			}
		}
	}
</script>

{#if userData}
	<div class="canvas-container" bind:this={container}>
		<Canvas size={{ width, height }}>
			<T.PerspectiveCamera
				makeDefault
				position={[maxDistance, maxDistance, maxDistance]}
				up={[0, 0, 1]}
				on:create={({ ref }) => {
					ref.lookAt(0, 0, 0);
				}}
			>
				<OrbitControls autoRotate />
			</T.PerspectiveCamera>

			<T.DirectionalLight position.y={10} position.z={10} />

			<T.Points>
				<T.BufferGeometry>
					<T.BufferAttribute
						args={[userData.vertices.data, 3]}
						attach={(parent, self) => {
							parent.setAttribute('position', self);
							return () => {};
						}}
					/>

					{#if userData.colors != null}
						<T.BufferAttribute
							args={[userData.colors.data, 3]}
							attach={(parent, self) => {
								parent.setAttribute('color', self);
								return () => {};
							}}
						/>
					{:else}
						<T.BufferAttribute
							args={[userData.vertices.data, 3]}
							attach={(parent, self) => {
								parent.setAttribute('color', self);
								return () => {};
							}}
						/>
					{/if}
				</T.BufferGeometry>

				<T.PointsMaterial size={pointSize} vertexColors={true} />
			</T.Points>

			<Grid
				type={'grid'}
				plane={'xy'}
				cellSize={0.1}
				gridSize={[1, 1]}
				cellThickness={0.5}
				sectionColor={'#aaa'}
				sectionSize={0}
			/>
			<T.AxesHelper />
		</Canvas>
	</div>
{/if}

<style>
	.canvas-container {
		/* width: 500px;
		height: 400px; */
		background-color: #888;
	}
</style>
