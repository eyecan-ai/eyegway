<script lang="ts">
	import { styleSettings } from '$lib/components/settings/StyleSettingsStore.js';
	import { Canvas, T } from '@threlte/core';
	import { Grid, OrbitControls } from '@threlte/extras';
	import type { DataPointCloud } from '../MosaicModel.js';

	export let userData: DataPointCloud | null = null;
	export let pointSize: number = 0.00001;
	export let width: number = 100;
	export let height: number = 100;
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

	$: if ($styleSettings.pcd.distance) {
		console.log('DISTANCE', $styleSettings.pcd.distance);
	}
</script>

{#if userData}
	<div
		class="canvas-container"
		bind:this={container}
		style={'background-color: ' + $styleSettings.pcd.background}
	>
		<Canvas size={{ width, height }} colorSpace={'srgb-linear'}>
			<T.PerspectiveCamera
				makeDefault
				fov={35}
				near={0.01}
				far={20000}
				position={[$styleSettings.pcd.distance / 3, 0, $styleSettings.pcd.distance / 3]}
				up={[0, 0, 1]}
				on:create={({ ref }) => {
					ref.lookAt(0, 0, 0);
				}}
			>
				<OrbitControls autoRotate />
			</T.PerspectiveCamera>

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

				<T.PointsMaterial size={$styleSettings.pcd.point_size} vertexColors={true} />
			</T.Points>

			<Grid
				type={'grid'}
				plane={'xy'}
				cellSize={$styleSettings.pcd.grid_tile}
				gridSize={[$styleSettings.pcd.grid_size, $styleSettings.pcd.grid_size]}
				cellThickness={1}
				sectionColor={'#aaa'}
				sectionSize={0}
				cellColor={$styleSettings.pcd.grid_color}
			/>
			<T.AxesHelper />
		</Canvas>
	</div>
{/if}

<style>
	.canvas-container {
		/* width: 500px;
		height: 400px; */
		background-color: #9e9e9e;
	}
</style>
