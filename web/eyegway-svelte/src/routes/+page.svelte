<script lang="ts">
	import HubControls from '$lib/components/hubs/HubControls.svelte';
	import Wall from '$lib/components/panels/Wall.svelte';
	import { styleSettings } from '$lib/components/panels/settings/SettingsStore.js';
	import { ThemeUtils } from 'svelte-tweakpane-ui';
	import { onMount } from 'svelte';

	// This is to keep updating CSS Variables when $styleSettings changes
	// to initialize them there's another similar function called in app.html
	import { updateCSSVariables } from '$lib/components/panels/settings/StyleSettingsUtils.js';
	$: updateCSSVariables($styleSettings);

	let sharedData: any[] = [];
	let editableMosaic: boolean = false;

	onMount(() => {
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

<div class="container is-fluid">
	<div class="box mb-1 mt-2 header">
		<div class="columns is-vcentered">
			<div class="column logo-container">
				<img
					src={$styleSettings.eyegway.logo ? $styleSettings.eyegway.logo : 'images/logo.png'}
					alt="Logo"
					class="logo"
				/>
			</div>
			<div class="column">
				<HubControls bind:data={sharedData} />
			</div>
		</div>
	</div>

	<div class="card p-0 mt-4 content">
		<Wall dataStream={sharedData} editMode={editableMosaic} />
	</div>
</div>

<style>
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
