<script lang="ts">
	import {
		Color,
		Pane,
		ThemeUtils,
		Image,
		type ImageValue,
		Slider,
		Separator,
		TabGroup,
		TabPage,
		type Theme
	} from 'svelte-tweakpane-ui';
	import { StyleSettings } from './SettingsModel.js';
	import { styleSettings } from './SettingsStore.js';
	import { onMount } from 'svelte';

	export let isDisabled: boolean = true;
	export let logoImage: ImageValue = $styleSettings.eyegway.logo;

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
		if (imageValue.src !== new StyleSettings().eyegway.logo) {
			// @ts-ignore
			convertBlobToBase64(imageValue?.src).then((value) => {
				if (value) $styleSettings.eyegway.logo = value;
				console.log('Logo image changed:', $styleSettings.eyegway.logo);
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

	let customTheme: Theme | undefined = undefined;
	let schemeRGB: { r: number; g: number; b: number };

	let borderLPercent: number;
	let textLPercent: number;
	let shadowLPercent: number;

	let primaryRGB: { r: number; g: number; b: number };
	let infoRGB: { r: number; g: number; b: number };
	let linkRGB: { r: number; g: number; b: number };
	let successRGB: { r: number; g: number; b: number };
	let warningRGB: { r: number; g: number; b: number };
	let dangerRGB: { r: number; g: number; b: number };

	onMount(() => {
		styleSettings.subscribe((value) => {
			logoImage = value.eyegway.logo;
			updateCSSVariables(value);
		});
		customTheme = {
			...{
				baseBackgroundColor: 'var(--bulma-body-background-color)',
				baseBorderRadius: '10px',
				baseFontFamily: 'sans-serif',
				baseShadowColor: 'var(--bulma-shadow)',
				bladeBorderRadius: '2px',
				bladeHorizontalPadding: '4px',
				bladeValueWidth: '180px',
				buttonBackgroundColor: 'var(--bulma-button-background)',
				buttonBackgroundColorActive: 'var(--bulma-button-background-active)',
				buttonBackgroundColorFocus: 'var(--bulma-button-background-focus)',
				buttonBackgroundColorHover: 'var(--bulma-button-background-hover)',
				buttonForegroundColor: 'var(--bulma-text)',
				containerBackgroundColor: 'var(--bulma-card-background-color)',
				containerBackgroundColorActive: 'var(--bulma-card-background-color-active)',
				containerBackgroundColorFocus: 'var(--bulma-card-background-color-focus)',
				containerBackgroundColorHover: 'var(--bulma-card-background-color-hover)',
				containerForegroundColor: 'var(--bulma-text)',
				containerHorizontalPadding: '4px',
				containerUnitSize: '20px',
				containerUnitSpacing: '4px',
				containerVerticalPadding: '4px',
				grooveForegroundColor: 'var(--bulma-groove-foreground)',
				inputBackgroundColor: 'var(--bulma-input-background)',
				inputBackgroundColorActive: 'var(--bulma-input-background-active)',
				inputBackgroundColorFocus: 'var(--bulma-input-background-focus)',
				inputBackgroundColorHover: 'var(--bulma-input-background-hover)',
				inputForegroundColor: 'var(--bulma-text)',
				labelForegroundColor: 'var(--bulma-text)',
				monitorBackgroundColor: 'var(--bulma-monitor-background)',
				monitorForegroundColor: 'var(--bulma-monitor-foreground)',
				pluginImageDraggingColor: 'var(--bulma-plugin-image-dragging)'
			}
		};

		schemeRGB = HSLStringToRGB(
			$styleSettings.bulma.scheme.h,
			$styleSettings.bulma.scheme.s,
			$styleSettings.bulma.scheme.main_l
		);

		borderLPercent = removePercent($styleSettings.bulma.border_l);
		textLPercent = removePercent($styleSettings.bulma.text_l);
		shadowLPercent = removePercent($styleSettings.bulma.shadow_l);

		primaryRGB = HSLStringToRGB(
			$styleSettings.bulma.primary.h,
			$styleSettings.bulma.primary.s,
			$styleSettings.bulma.primary.l
		);
		infoRGB = HSLStringToRGB(
			$styleSettings.bulma.info.h,
			$styleSettings.bulma.info.s,
			$styleSettings.bulma.info.l
		);
		linkRGB = HSLStringToRGB(
			$styleSettings.bulma.link.h,
			$styleSettings.bulma.link.s,
			$styleSettings.bulma.link.l
		);
		successRGB = HSLStringToRGB(
			$styleSettings.bulma.success.h,
			$styleSettings.bulma.success.s,
			$styleSettings.bulma.success.l
		);
		warningRGB = HSLStringToRGB(
			$styleSettings.bulma.warning.h,
			$styleSettings.bulma.warning.s,
			$styleSettings.bulma.warning.l
		);
		dangerRGB = HSLStringToRGB(
			$styleSettings.bulma.danger.h,
			$styleSettings.bulma.danger.s,
			$styleSettings.bulma.danger.l
		);
	});

	$: if (customTheme) ThemeUtils.setGlobalDefaultTheme(customTheme);

	function removePercent(value: string): number {
		return parseFloat(value.replace('%', ''));
	}

	function removeDeg(value: string): number {
		return parseFloat(value.replace('deg', ''));
	}
	function RGBToHSLString(r: number, g: number, b: number) {
		const out = RGBToHSL(r, g, b);
		return { h: `${out.h * 360}deg`, s: `${out.s * 100}%`, l: `${out.l * 100}%` };
	}
	function HSLStringToRGB(h: string, s: string, l: string) {
		return HSLToRGB(removeDeg(h) / 360, removePercent(s) / 100, removePercent(l) / 100);
	}
	function RGBToHSL(r: number, g: number, b: number) {
		r /= 255;
		g /= 255;
		b /= 255;

		const max = Math.max(r, g, b),
			min = Math.min(r, g, b);

		let h = 0,
			s = 0,
			l = (max + min) / 2;

		if (max === min) {
			h = s = 0; // achromatic
		} else {
			const d = max - min;
			s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
			switch (max) {
				case r:
					h = (g - b) / d + (g < b ? 6 : 0);
					break;
				case g:
					h = (b - r) / d + 2;
					break;
				case b:
					h = (r - g) / d + 4;
					break;
			}
			h /= 6;
		}

		return { h: h, s: s, l: l };
	}

	function HSLToRGB(h: number, s: number, l: number) {
		let r: number, g: number, b: number;

		if (s === 0) {
			r = g = b = l; // achromatic
		} else {
			const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
			const p = 2 * l - q;
			const hue2rgb = (p: number, q: number, t: number) => {
				if (t < 0) t += 1;
				if (t > 1) t -= 1;
				if (t < 1 / 6) return p + (q - p) * 6 * t;
				if (t < 1 / 2) return q;
				if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
				return p;
			};
			r = hue2rgb(p, q, h + 1 / 3);
			g = hue2rgb(p, q, h);
			b = hue2rgb(p, q, h - 1 / 3);
		}

		return {
			r: Math.round(r * 255),
			g: Math.round(g * 255),
			b: Math.round(b * 255)
		};
	}

	let innerWidth: number = 0;
	let innerHeight: number = 0;
	let paneWidth: number = 500;
</script>

<svelte:window bind:innerWidth bind:innerHeight />
{#if !isDisabled}
	<Pane
		position={'draggable'}
		title="Style Settings"
		scale={1.5}
		x={(innerWidth - paneWidth) / 2}
		y={innerHeight / 2 - 200}
		userExpandable={false}
		resizable={false}
		width={paneWidth}
	>
		<TabGroup>
			<TabPage title="General">
				<Image
					bind:value={logoImage}
					fit="contain"
					label="Logo Image"
					on:change={() => {
						handleLogoImageChange(logoImage);
					}}
				/>
				<Color
					bind:value={schemeRGB}
					label="Main Accent Color"
					on:change={() => {
						const out = RGBToHSLString(schemeRGB.r, schemeRGB.g, schemeRGB.b);
						$styleSettings.bulma.scheme = { h: out.h, s: out.s, main_l: out.l };
					}}
				/>
				<Color
					bind:value={$styleSettings.eyegway.header['background-color']}
					label="Header Background Color"
				/>
				<Color
					bind:value={$styleSettings.eyegway.panel['background-color']}
					label="Panel Background Color"
				/>
				<Color
					bind:value={$styleSettings.eyegway.content['background-color']}
					label="Content Background Color"
				/>
				<Color
					bind:value={$styleSettings.eyegway.background['first-color']}
					label="Internal Gradient Background Color"
				/>
				<Color
					bind:value={$styleSettings.eyegway.background['second-color']}
					label="External Gradient Background Color"
				/>
				<Separator />
				<Slider
					bind:value={borderLPercent}
					min={0}
					max={100}
					label="Border Brightness"
					format={(v) => v.toFixed(0)}
					on:change={() => {
						$styleSettings.bulma.border_l = borderLPercent + '%';
					}}
				/>
				<Slider
					bind:value={textLPercent}
					min={0}
					max={100}
					label="Text Brightness"
					format={(v) => v.toFixed(0)}
					on:change={() => {
						$styleSettings.bulma.text_l = textLPercent + '%';
						$styleSettings.bulma.text_strong_l = textLPercent + 19 + '%';
						$styleSettings.bulma.text_weak_l = textLPercent - 8 + '%';
					}}
				/>
				<Slider
					bind:value={shadowLPercent}
					min={0}
					max={100}
					label="Shadow Brightness"
					format={(v) => v.toFixed(0)}
					on:change={() => {
						$styleSettings.bulma.shadow_l = shadowLPercent + '%';
					}}
				/>
			</TabPage>
			<TabPage title="Buttons">
				<Color
					bind:value={primaryRGB}
					label="Primary Color"
					on:change={() => {
						const out = RGBToHSLString(primaryRGB.r, primaryRGB.g, primaryRGB.b);
						$styleSettings.bulma.primary = { h: out.h, s: out.s, l: out.l };
					}}
				/>
				<Color
					bind:value={infoRGB}
					label="Info Color"
					on:change={() => {
						const out = RGBToHSLString(infoRGB.r, infoRGB.g, infoRGB.b);
						$styleSettings.bulma.info = { h: out.h, s: out.s, l: out.l };
					}}
				/>
				<Color
					bind:value={linkRGB}
					label="Link Color"
					on:change={() => {
						const out = RGBToHSLString(linkRGB.r, linkRGB.g, linkRGB.b);
						$styleSettings.bulma.link = { h: out.h, s: out.s, l: out.l };
					}}
				/>
				<Color
					bind:value={successRGB}
					label="Success Color"
					on:change={() => {
						const out = RGBToHSLString(successRGB.r, successRGB.g, successRGB.b);
						$styleSettings.bulma.success = { h: out.h, s: out.s, l: out.l };
					}}
				/>
				<Color
					bind:value={warningRGB}
					label="Warning Color"
					on:change={() => {
						const out = RGBToHSLString(warningRGB.r, warningRGB.g, warningRGB.b);
						$styleSettings.bulma.warning = { h: out.h, s: out.s, l: out.l };
					}}
				/>
				<Color
					bind:value={dangerRGB}
					label="Danger Color"
					on:change={() => {
						const out = RGBToHSLString(dangerRGB.r, dangerRGB.g, dangerRGB.b);
						$styleSettings.bulma.danger = { h: out.h, s: out.s, l: out.l };
					}}
				/>
			</TabPage>
		</TabGroup>
	</Pane>
{/if}
