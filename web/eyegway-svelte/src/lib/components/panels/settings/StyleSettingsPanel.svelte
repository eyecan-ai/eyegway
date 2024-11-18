<script lang="ts">
	import {
		Button,
		Color,
		Folder,
		Pane,
		ThemeUtils,
		Image,
		type ImageValue
	} from 'svelte-tweakpane-ui';
	import { styleSettings, styleSettingsReset, StyleSettings } from './StyleSettingsStore.js';
	import { onMount } from 'svelte';

	let logoImage: ImageValue = 'images/logo.png';

	export function updateCSSVariables(styles: StyleSettings, prefix = '') {
		if (typeof document === 'undefined') return;

		for (const [key, value] of Object.entries(styles)) {
			if (typeof value === 'object' && value !== null) {
				updateCSSVariables(value, `${prefix}${key}-`);
			} else {
				const cssVarName = `--${prefix}${key.replace(/_/g, '-')}`;
				document.documentElement.style.setProperty(cssVarName, value);
			}
		}
	}

	onMount(() => {
		// Update CSS variables when the style settings change
		styleSettings.subscribe((value) => {
			updateCSSVariables(value);
		});
	});

	// Continuously update the logo image when it changes
	// @ts-ignore
	$: $styleSettings.color.logo = logoImage?.src;
</script>

<Pane position={'inline'} theme={ThemeUtils.presets.jetblack} width={350}>
	<Folder title="Global Settings">
		<Image bind:value={logoImage} fit="contain" label="Image" />
		<Color bind:value={$styleSettings.color.panel} label="Panel Color" />
		<Color bind:value={$styleSettings.color.panel_unselected} label="Empty Panel Color" />
		<Color bind:value={$styleSettings.color.header} label="Header Color" />
		<Color bind:value={$styleSettings.color.header_buttons} label="Header Buttons Color" />
		<Color bind:value={$styleSettings.color.container} label="Panels Container Color" />
		<Color bind:value={$styleSettings.color.internal_gradient} label="Gradient Start Color" />
		<Color bind:value={$styleSettings.color.external_gradient} label="Gradient End Color" />
	</Folder>
	<Folder title="">
		<Button on:click={styleSettingsReset} title="Reset Defaults" />
	</Folder>
</Pane>
