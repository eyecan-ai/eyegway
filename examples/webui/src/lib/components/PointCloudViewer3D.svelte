<script lang="ts">
	import { encode, decode, ExtensionCodec } from '@msgpack/msgpack';
	import { Canvas, T } from '@threlte/core';
	import { Align, Grid, OrbitControls } from '@threlte/extras';
	import { onMount } from 'svelte';
	import TPointCloud from './TPointCloud.svelte';
	import { resize } from '$lib/utils/resize';

	const size = 20;
	export let data: any = null;
	export let vertices: Float32Array | null = null;
	export let colors: Float32Array | null = null;
	export let width: number = 100;
	export let height: number = 100;
	let maxDistance = 1;

	onMount(() => {
		// console.log("Vertices"	,vertices,colors);
	});

	$: {
		if (data) {
			const array = data.data;
			if (data.shape.length != 2) {
				throw new Error('Data shape must be 2');
			}
			const [rows, cols] = data.shape;

			const N = array.length / cols;
			vertices = new Float32Array(N * 3);
			colors = new Float32Array(N * 3);

			for (let i = 0; i < N; i++) {
				vertices[i * 3] = array[i * cols];
				vertices[i * 3 + 1] = array[i * cols + 1];
				vertices[i * 3 + 2] = array[i * cols + 2];
				colors[i * 3] = array[i * cols + 3] / 255;
				colors[i * 3 + 1] = array[i * cols + 4] / 255;
				colors[i * 3 + 2] = array[i * cols + 5] / 255;
			}
		}
	}

	function onResize(el) {
		// width = canvasContainer.clientWidth;
		// height = canvasContainer.clientHeight;
		console.log('RESIZE', el.contentRect);
		width = el.contentRect.width;
		height = el.contentRect.height;
	}

	// Set width/height based on canvas-container resize event
	let canvasContainer: HTMLCanvasElement;
	$: {
		if (canvasContainer) {
			width = canvasContainer.clientWidth;
			height = canvasContainer.clientHeight;
		}
		// add resize event handler to canvas-container
		if (canvasContainer) {
			// canvasContainer.removeEventListener('resize', onResize);
			canvasContainer.addEventListener('resize', onResize);
			console.log('ADDED RESIZE');
		}
	}
</script>

<div class="canvas-container" use:resize={onResize}>
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
		<TPointCloud {vertices} {colors} pointSize={0.01} vertexColors={true} />

		<!-- <T.Points>
			<T.BufferGeometry>
				<T.BufferAttribute
					args={[vertices, 3]}
					attach={(parent, self) => {
						parent.setAttribute('position', self);
						return () => {
							// cleanup function called when ref changes or the component unmounts
							// https://threlte.xyz/docs/reference/core/t#attach
						};
					}}
				/>
				<T.BufferAttribute
					args={[colors, 3]}
					attach={(parent, self) => {
						parent.setAttribute('color', self);
						return () => {
							// cleanup function called when ref changes or the component unmounts
							// https://threlte.xyz/docs/reference/core/t#attach
						};
					}}
				/>
			</T.BufferGeometry>
			<T.PointsMaterial size={0.01} vertexColors={true} />
		</T.Points> -->

		<!-- <T.GridHelper args={[1, 1, 10, 10]} rotation={[Math.PI / 2, 0, 0]} /> -->
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

<style>
	.canvas-container {
		/* width: 500px;
		height: 400px; */
		background-color: #888;
	}
</style>
