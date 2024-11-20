<script lang="ts">
	import { Canvas, T } from '@threlte/core';
	import { Grid, OrbitControls } from '@threlte/extras';
	import type { DataPointCloud } from '../PaneModel.js';
	import type { PointCloudSettings } from '../settings/SettingsModel.js';

	export let userData: DataPointCloud | null = null;
	export let userSettings: PointCloudSettings | null = null;
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
</script>

{#if userData && userSettings}
	<div
		class="canvas-container"
		bind:this={container}
		style={'background-color: ' + userSettings.background}
	>
		<Canvas size={{ width, height }} colorSpace={'srgb-linear'}>
			<T.PerspectiveCamera
				makeDefault
				fov={35}
				near={0.01}
				far={20000}
				position={[userSettings.distance, userSettings.distance, userSettings.distance]}
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

				<T.PointsMaterial size={userSettings.point_size} vertexColors={true} />
			</T.Points>

			<Grid
				type={'grid'}
				plane={'xy'}
				cellSize={userSettings.grid_tile}
				gridSize={[userSettings.grid_size, userSettings.grid_size]}
				cellThickness={1}
				sectionColor={'#aaa'}
				sectionSize={0}
				cellColor={userSettings.grid_color}
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
