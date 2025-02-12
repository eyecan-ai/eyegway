<script lang="ts">
	import HubControls from '$lib/components/hubs/HubControls.svelte';
	import Wall from '$lib/components/panels/Wall.svelte';
	import { StyleConfigurationUtils } from '$lib/components/panels/style/StyleConfigurationUtils.js';
	import { ThemeUtils } from 'svelte-tweakpane-ui';
	import { onMount } from 'svelte';
	import { type Writable } from 'svelte/store';

	import { ChevronDown, X } from 'lucide-svelte';

	// This is to keep updating CSS Variables when $styleSettings changes
	// to initialize them there's another similar function called in app.html
	import { updateCSSVariables } from '$lib/components/panels/style/StyleConfigurationPanel.js';
	import type { StyleConfiguration } from '$lib/components/panels/style/StyleModel.js';

	let sharedData: any[] = [];
	let editableMosaic: boolean = false;
	let showControls: boolean = false;

	let styleConfiguration: Writable<StyleConfiguration>;
	let styleUtils = new StyleConfigurationUtils();

	$: if (styleConfiguration) {
		updateCSSVariables($styleConfiguration);
	}

	onMount(() => {
		styleUtils.getStore().then((config) => {
			styleConfiguration = config;
		});
		const customTheme = {
			...{
				baseBackgroundColor:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), calc(var(--bulma-scheme-main-l) - 2%))',
				baseBorderRadius: 'var(--bulma-control-radius)',
				baseFontFamily: 'var(--bulma-family-primary)',
				baseShadowColor: 'var(--bulma-shadow)',
				bladeBorderRadius: 'var(--bulma-radius-small)',
				buttonBackgroundColor:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), var(--bulma-text-strong-l))',
				buttonBackgroundColorActive:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), var(--bulma-text-l))',
				buttonBackgroundColorFocus:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), var(--bulma-text-weak-l))',
				buttonBackgroundColorHover:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), var(--bulma-text-weak-l))',
				buttonForegroundColor:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), var(--bulma-scheme-main-l))',
				containerBackgroundColor:
					'rgba(var(--eyegway-header-background-color-r), var(--eyegway-header-background-color-g), var(--eyegway-header-background-color-b), 0.2)',
				containerBackgroundColorActive:
					'rgba(var(--eyegway-header-background-color-r), var(--eyegway-header-background-color-g), var(--eyegway-header-background-color-b), 0.35)',
				containerBackgroundColorFocus:
					'rgba(var(--eyegway-header-background-color-r), var(--eyegway-header-background-color-g), var(--eyegway-header-background-color-b), 0.3)',
				containerBackgroundColorHover:
					'rgba(var(--eyegway-header-background-color-r), var(--eyegway-header-background-color-g), var(--eyegway-header-background-color-b), 0.25)',
				containerForegroundColor: 'var(--bulma-text)',
				grooveForegroundColor: 'var(--bulma-border)',
				inputBackgroundColor:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), calc(var(--bulma-scheme-main-l) + 2%))',
				inputBackgroundColorActive:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), calc(var(--bulma-scheme-main-l) + 2%))',
				inputBackgroundColorFocus:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), calc(var(--bulma-scheme-main-l) + 3%))',
				inputBackgroundColorHover:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), calc(var(--bulma-scheme-main-l) + 4%))',
				inputForegroundColor: 'var(--bulma-text-strong)',
				labelForegroundColor: 'var(--bulma-text-strong)',
				monitorBackgroundColor:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), calc(var(--bulma-scheme-main-l) + 2%))',
				monitorForegroundColor: 'var(--bulma-text-strong)',
				pluginImageDraggingColor:
					'hsl(var(--bulma-scheme-h), var(--bulma-scheme-s), calc(var(--bulma-scheme-main-l) + 2%)'
			}
		};

		ThemeUtils.setGlobalDefaultTheme(customTheme);
	});
</script>

<div class="container my-fluid-container">
	<div class="box mb-1 mt-2 header">
		<div class="columns {showControls ? '' : 'is-mobile'}">
			<div class="column is-flex is-justify-content-space-between">
				{#if styleConfiguration}
					<img
						src={$styleConfiguration.eyegway.logo
							? $styleConfiguration.eyegway.logo
							: 'images/eyegway-logo.svg'}
						alt="Logo"
						class="logo"
					/>
				{/if}
				<button
					class="button is-small is-hidden-tablet"
					class:is-active={showControls}
					on:click={() => (showControls = !showControls)}
				>
					{#if showControls}
						<X strokeWidth={1} />
					{:else}
						<ChevronDown strokeWidth={1} />
					{/if}
				</button>
			</div>
			<div
				class="column is-flex is-justify-content-flex-end {showControls ? '' : 'is-hidden-mobile'}"
			>
				<div class="is-flex is-justify-content-right">
					<HubControls bind:data={sharedData} />
				</div>
			</div>
		</div>
	</div>

	<div class="card p-0 mt-4 content">
		<Wall dataStream={sharedData} editMode={editableMosaic} />
	</div>
</div>

<style>
	.container.my-fluid-container {
		max-width: none !important;
		width: 100%;
	}

	@media screen and (min-width: 1024px) {
		.container.my-fluid-container {
			padding-left: 32px;
			padding-right: 32px;
		}
	}
	.header {
		background-color: rgba(
			var(--eyegway-header-background-color-r),
			var(--eyegway-header-background-color-g),
			var(--eyegway-header-background-color-b),
			var(--eyegway-header-background-color-a)
		);
	}
	.content {
		flex-grow: 1;
		height: 100%;
		width: 100%;
		background-color: rgba(
			var(--eyegway-content-background-color-r),
			var(--eyegway-content-background-color-g),
			var(--eyegway-content-background-color-b),
			var(--eyegway-content-background-color-a)
		);
	}
	.container {
		display: flex;
		flex-direction: column;
		height: 100vh;
		padding-bottom: 50px;
	}
	.logo {
		display: flex;
		height: 30px;
		align-items: center;
		padding-left: 25px;
	}
</style>
