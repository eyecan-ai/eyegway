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
	import { styleSettings } from './SettingsStore.js';
	import {
		HSLStringToRGB,
		RGBToHSLString,
		removePercent,
		convertBlobToBase64,
		updateCSSVariables
	} from './StyleSettingsUtils.js';
	import { onMount } from 'svelte';

	export let isDisabled: boolean = true;

	let logoImage: ImageValue;

	let customTheme: Theme;
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
		customTheme = {
			...{
				baseBackgroundColor: 'var(--bulma-body-background-color)',
				baseBorderRadius: 'var(--bulma-radius)',
				baseFontFamily: 'var(--bulma-family-primary)',
				baseShadowColor: 'var(--bulma-shadow-color)',
				bladeBorderRadius: 'var(--bulma-radius-small)',
				bladeHorizontalPadding: 'var(--bulma-block-spacing)',
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
				inputBackgroundColor: 'var(--bulma-input-background-color)',
				inputBackgroundColorActive: 'var(--bulma-input-background-color-active)',
				inputBackgroundColorFocus: 'var(--bulma-input-background-color-focus)',
				inputBackgroundColorHover: 'var(--bulma-input-background-color-hover)',
				inputForegroundColor: 'var(--bulma-input-color)',
				labelForegroundColor: 'var(--bulma-label-color)',
				monitorBackgroundColor: 'var(--bulma-background)',
				monitorForegroundColor: 'var(--bulma-text)',
				pluginImageDraggingColor: 'var(--bulma-background)'
			}
		};
		ThemeUtils.setGlobalDefaultTheme(customTheme);

		styleSettings.subscribe((value) => {
			logoImage = value.eyegway.logo;

			schemeRGB = HSLStringToRGB(
				value.bulma.scheme.h,
				value.bulma.scheme.s,
				value.bulma.scheme.main_l
			);

			borderLPercent = removePercent(value.bulma.border_l);
			textLPercent = removePercent(value.bulma.text_l);
			shadowLPercent = removePercent(value.bulma.shadow_l);

			primaryRGB = HSLStringToRGB(
				value.bulma.primary.h,
				value.bulma.primary.s,
				value.bulma.primary.l
			);
			infoRGB = HSLStringToRGB(value.bulma.info.h, value.bulma.info.s, value.bulma.info.l);
			linkRGB = HSLStringToRGB(value.bulma.link.h, value.bulma.link.s, value.bulma.link.l);
			successRGB = HSLStringToRGB(
				value.bulma.success.h,
				value.bulma.success.s,
				value.bulma.success.l
			);
			warningRGB = HSLStringToRGB(
				value.bulma.warning.h,
				value.bulma.warning.s,
				value.bulma.warning.l
			);
			dangerRGB = HSLStringToRGB(value.bulma.danger.h, value.bulma.danger.s, value.bulma.danger.l);

			updateCSSVariables(value);
		});
	});

	let innerWidth: number = 0;
	let innerHeight: number = 0;
	let paneWidth: number = 400;
</script>

<svelte:window bind:innerWidth bind:innerHeight />
{#if !isDisabled}
	<Pane
		position={'draggable'}
		title="Style Settings"
		scale={1}
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
						if (logoImage instanceof HTMLImageElement && logoImage.src) {
							convertBlobToBase64(logoImage.src).then((value) => {
								if (value) $styleSettings.eyegway.logo = value;
							});
						}

						logoImage = $styleSettings.eyegway.logo;
					}}
				/>
				<Color
					bind:value={schemeRGB}
					label="Main Accent Color"
					on:change={() => {
						const out = RGBToHSLString(schemeRGB.r, schemeRGB.g, schemeRGB.b);
						$styleSettings.bulma.scheme = { h: out.h, s: out.s, main_l: out.l };

						schemeRGB = HSLStringToRGB(
							$styleSettings.bulma.scheme.h,
							$styleSettings.bulma.scheme.s,
							$styleSettings.bulma.scheme.main_l
						);
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
					label="Internal Body Background Color"
				/>
				<Color
					bind:value={$styleSettings.eyegway.background['second-color']}
					label="External Body Background Color"
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

						borderLPercent = removePercent($styleSettings.bulma.border_l);
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

						textLPercent = removePercent($styleSettings.bulma.text_l);
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

						shadowLPercent = removePercent($styleSettings.bulma.shadow_l);
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

						primaryRGB = HSLStringToRGB(
							$styleSettings.bulma.primary.h,
							$styleSettings.bulma.primary.s,
							$styleSettings.bulma.primary.l
						);
					}}
				/>
				<Color
					bind:value={infoRGB}
					label="Info Color"
					on:change={() => {
						const out = RGBToHSLString(infoRGB.r, infoRGB.g, infoRGB.b);
						$styleSettings.bulma.info = { h: out.h, s: out.s, l: out.l };

						infoRGB = HSLStringToRGB(
							$styleSettings.bulma.info.h,
							$styleSettings.bulma.info.s,
							$styleSettings.bulma.info.l
						);
					}}
				/>
				<Color
					bind:value={linkRGB}
					label="Link Color"
					on:change={() => {
						const out = RGBToHSLString(linkRGB.r, linkRGB.g, linkRGB.b);
						$styleSettings.bulma.link = { h: out.h, s: out.s, l: out.l };

						linkRGB = HSLStringToRGB(
							$styleSettings.bulma.link.h,
							$styleSettings.bulma.link.s,
							$styleSettings.bulma.link.l
						);
					}}
				/>
				<Color
					bind:value={successRGB}
					label="Success Color"
					on:change={() => {
						const out = RGBToHSLString(successRGB.r, successRGB.g, successRGB.b);
						$styleSettings.bulma.success = { h: out.h, s: out.s, l: out.l };

						successRGB = HSLStringToRGB(
							$styleSettings.bulma.success.h,
							$styleSettings.bulma.success.s,
							$styleSettings.bulma.success.l
						);
					}}
				/>
				<Color
					bind:value={warningRGB}
					label="Warning Color"
					on:change={() => {
						const out = RGBToHSLString(warningRGB.r, warningRGB.g, warningRGB.b);
						$styleSettings.bulma.warning = { h: out.h, s: out.s, l: out.l };

						warningRGB = HSLStringToRGB(
							$styleSettings.bulma.warning.h,
							$styleSettings.bulma.warning.s,
							$styleSettings.bulma.warning.l
						);
					}}
				/>
				<Color
					bind:value={dangerRGB}
					label="Danger Color"
					on:change={() => {
						const out = RGBToHSLString(dangerRGB.r, dangerRGB.g, dangerRGB.b);
						$styleSettings.bulma.danger = { h: out.h, s: out.s, l: out.l };

						dangerRGB = HSLStringToRGB(
							$styleSettings.bulma.danger.h,
							$styleSettings.bulma.danger.s,
							$styleSettings.bulma.danger.l
						);
					}}
				/>
			</TabPage>
		</TabGroup>
	</Pane>
{/if}
