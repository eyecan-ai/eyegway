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
				baseBackgroundColor: 'var(--bulma-body-background-color)',
				baseBorderRadius: 'var(--bulma-control-radius)',
				baseFontFamily: 'var(--bulma-family-primary)',
				baseShadowColor: 'var(--bulma-shadow-color)',
				bladeBorderRadius: 'var(--bulma-radius-small)',
				// bladeHorizontalPadding: 'var(--bulma-block-spacing)',
				buttonBackgroundColor: 'var(--bulma-button-background-color)',
				buttonBackgroundColorActive: 'var(--bulma-button-background-color-active)',
				buttonBackgroundColorFocus: 'var(--bulma-button-background-color-focus)',
				buttonBackgroundColorHover: 'var(--bulma-button-background-color-hover)',
				buttonForegroundColor: 'var(--bulma-button-color)',
				containerBackgroundColor: 'var(--bulma-card-background-color)',
				containerBackgroundColorActive: 'var(--bulma-card-background-color-active)',
				containerBackgroundColorFocus: 'var(--bulma-card-background-color-focus)',
				containerBackgroundColorHover: 'var(--bulma-card-background-color-hover)',
				containerForegroundColor: 'var(--bulma-card-color)',
				containerHorizontalPadding: 'var(--bulma-card-padding)',
				containerVerticalPadding: 'var(--bulma-card-padding)',
				grooveForegroundColor: 'var(--bulma-border)',
				inputBackgroundColor:
					'hsl(var(--bulma-input-h),var(--bulma-input-s),calc(var(--bulma-input-background-l) + var(--bulma-input-background-l-delta)))',
				inputBackgroundColorActive: 'var(--bulma-input-background-color-active)',
				inputBackgroundColorFocus: 'var(--bulma-input-background-color-focus)',
				inputBackgroundColorHover: 'var(--bulma-input-background-color-hover)',
				inputForegroundColor: 'var(--bulma-text)',
				labelForegroundColor: 'var(--bulma-text)',
				monitorBackgroundColor: 'var(--bulma-background)',
				monitorForegroundColor: 'var(--bulma-text)',
				pluginImageDraggingColor: 'var(--bulma-background)'
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
