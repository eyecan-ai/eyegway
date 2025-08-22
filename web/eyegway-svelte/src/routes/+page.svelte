<script lang="ts">
	import HubControls from '$lib/components/hubs/HubControls.svelte';
	import Wall from '$lib/components/panels/Wall.svelte';
	import { StyleConfigurationUtils } from '$lib/components/panels/style/StyleConfigurationUtils.js';
	import { ThemeUtils } from 'svelte-tweakpane-ui';
	import { onMount } from 'svelte';
	import { type Writable } from 'svelte/store';
    import { Parameters } from '$lib/Parameters.js';
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
	<!-- Header -->
    <div class="box mb-1 mt-2 header">
		<div class="columns is-flex is-vcentered is-multiline">
            <!-- Desktop layout -->
            <!-- [LOGO][-------TITLE-------][CONTROLS] -->

            <!-- Mobile layout (controls not toggled) -->
            <!-- [LOGO]       [v] -->

            <!-- Mobile layout (controls toggled) -->
            <!-- [LOGO]       [X] -->
            <!-- [---CONTROLS---] -->

            <!-- Logo: left-justified and "is-narrow" to avoid extra margin -->
			{#if styleConfiguration}
				<div class="column is-justify-content-left is-narrow">
					<img
						src={$styleConfiguration.eyegway.logo
							? $styleConfiguration.eyegway.logo
							: 'images/eyegway-logo.svg'}
						alt="Logo"
						class="logo"
					/>
				</div>
			{/if}

            <!-- Title (only desktop): centered and taking all the available space -->
			{#if Parameters.title}
				<div class="column has-text-centered is-hidden-mobile">
					<span class="title is-4">{Parameters.title}</span>
				</div>
			{/if}

			<!-- Controls toggle button (only mobile): right-justified ans "is-narrow" to avoid extra margin -->
			<div class="column controls-toggle-column is-narrow is-hidden-desktop is-justify-content-right">
				<button
					class="button is-small"
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

			<!-- HubControls (see CSS at the bottom for style) -->
			<div class="column hubcontrols-container" class:show-controls={showControls}>
				<HubControls bind:data={sharedData} />
			</div>
		</div>
	</div>

    <!-- Main content area -->
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
		height: 100dvh;
		padding-bottom: 50px;
	}

	.logo {
		display: flex;
		height: 30px;
		align-items: center;
	}

	/* HubControls settings (Mobile layout) */
	.hubcontrols-container {
		display: none;  /* hidden by default */
		width: 100%;
		justify-content: center;
        /* the next two lines ensure that controls go on a new line */
        flex: 0 0 100%;
		order: 4; 
	}
	.hubcontrols-container.show-controls {
		display: flex;  /* show when toggled */
	}
	.controls-toggle-column {
		display: flex;
		justify-content: flex-end;
        flex: none;
	}

	/* Desktop layout */
	@media screen and (min-width: 1024px) {
		.hubcontrols-container {
            display: flex !important;  /* always visible on desktop */
            justify-content: flex-end;
            flex: none; /* reset to normal flex behavior (if switching from mobile) */
            max-width: none; /* no forced width */
            width: auto; /* shrink to fit */
            order: 3; /* inline in header row */
        }
		.controls-toggle-column {
			display: none; /* no controls toggle on desktop */
		}
	}
</style>
