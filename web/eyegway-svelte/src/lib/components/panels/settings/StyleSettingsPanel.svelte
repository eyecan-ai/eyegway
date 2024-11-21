<script lang="ts">
	import { Color, Pane, ThemeUtils, Image, type ImageValue, List } from 'svelte-tweakpane-ui';
	import { StyleSettings } from './SettingsModel.js';
	import { styleSettings } from './SettingsStore.js';
	import { onMount } from 'svelte';

	export let isDisabled: boolean = true;
	export let logoImage: ImageValue = $styleSettings.color.logo;

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

	function handleLogoImageChange(imageValue: ImageValue) {
		// @ts-ignore
		if (imageValue.src !== new StyleSettings().color.logo) {
			// @ts-ignore
			convertBlobToBase64(imageValue?.src).then((value) => {
				if (value) $styleSettings.color.logo = value;
				console.log('Logo image changed:', $styleSettings.color.logo);
			});
		}
	}

	async function convertBlobToBase64(blobUrl: string): Promise<string> {
		try {
			const response = await fetch(blobUrl);
			if (!response.ok) {
				throw new Error(`Failed to fetch blob: ${response.statusText}`);
			}
			const blob = await response.blob();
			return new Promise((resolve, reject) => {
				const reader = new FileReader();
				reader.onloadend = () => resolve(reader.result as string);
				reader.onerror = () => reject('Error converting blob to Base64');
				reader.readAsDataURL(blob);
			});
		} catch (error) {
			console.error(error);
			return '';
		}
	}

	onMount(() => {
		styleSettings.subscribe((value) => {
			logoImage = value.color.logo;
			ThemeUtils.setGlobalDefaultTheme(ThemeUtils.presets[value.color.settings_theme]);
			updateCSSVariables(value);
		});
	});

	let innerWidth: number = 0;
	let innerHeight: number = 0;
	let paneWidth: number = 500;
</script>

<svelte:window bind:innerWidth bind:innerHeight />
{#if !isDisabled}
	<Pane
		position={'draggable'}
		title="Style Settings"
		scale={1.2}
		x={(innerWidth - paneWidth) / 2}
		y={innerHeight / 2 - 200}
		userExpandable={false}
		resizable={false}
		theme={ThemeUtils.presets[$styleSettings.color.settings_theme]}
		width={paneWidth}
	>
		<Image
			bind:value={logoImage}
			fit="contain"
			label="Logo Image"
			on:change={() => {
				handleLogoImageChange(logoImage);
			}}
		/>
		<Color bind:value={$styleSettings.color.header} label="Header Color" />
		<Color bind:value={$styleSettings.color.header_buttons} label="Header Buttons Color" />
		<Color bind:value={$styleSettings.color.panel} label="Panel Color" />
		<Color bind:value={$styleSettings.color.container} label="Panels Container Color" />
		<Color bind:value={$styleSettings.color.internal_gradient} label="Background Center Color" />
		<Color bind:value={$styleSettings.color.external_gradient} label="Background Border Color" />
		<List
			bind:value={$styleSettings.color.settings_theme}
			label="Settings Theme"
			options={Object.keys(ThemeUtils.presets)}
		/>
	</Pane>
{/if}
