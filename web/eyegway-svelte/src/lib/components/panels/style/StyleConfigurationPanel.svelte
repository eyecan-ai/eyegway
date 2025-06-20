<script lang="ts">
	import {
		Color,
		Pane,
		Image,
		type ImageValue,
		Slider,
		Separator,
		TabGroup,
		TabPage,
	} from 'svelte-tweakpane-ui';
	import {
		HSLStringToRGB,
		RGBToHSLString,
		removePercent,
		convertBlobToBase64
	} from './StyleConfigurationPanel.js';
	import { onMount } from 'svelte';
	import type { StyleConfiguration } from './StyleModel.js';

	export let styleConfiguration: StyleConfiguration;
	export let isDisabled: boolean = true;

	let logoImage: ImageValue;

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

	export let refresh: boolean = false;

	onMount(() => {
		refresh = true;
	});

	$: if (refresh) {
		logoImage = $styleConfiguration.eyegway.logo;

		schemeRGB = HSLStringToRGB(
			$styleConfiguration.bulma.scheme.h,
			$styleConfiguration.bulma.scheme.s,
			$styleConfiguration.bulma.scheme.main_l
		);

		borderLPercent = removePercent($styleConfiguration.bulma.border_l);
		textLPercent = removePercent($styleConfiguration.bulma.text_l);
		shadowLPercent = removePercent($styleConfiguration.bulma.shadow_l);

		primaryRGB = HSLStringToRGB(
			$styleConfiguration.bulma.primary.h,
			$styleConfiguration.bulma.primary.s,
			$styleConfiguration.bulma.primary.l
		);
		infoRGB = HSLStringToRGB(
			$styleConfiguration.bulma.info.h,
			$styleConfiguration.bulma.info.s,
			$styleConfiguration.bulma.info.l
		);
		linkRGB = HSLStringToRGB(
			$styleConfiguration.bulma.link.h,
			$styleConfiguration.bulma.link.s,
			$styleConfiguration.bulma.link.l
		);
		successRGB = HSLStringToRGB(
			$styleConfiguration.bulma.success.h,
			$styleConfiguration.bulma.success.s,
			$styleConfiguration.bulma.success.l
		);
		warningRGB = HSLStringToRGB(
			$styleConfiguration.bulma.warning.h,
			$styleConfiguration.bulma.warning.s,
			$styleConfiguration.bulma.warning.l
		);
		dangerRGB = HSLStringToRGB(
			$styleConfiguration.bulma.danger.h,
			$styleConfiguration.bulma.danger.s,
			$styleConfiguration.bulma.danger.l
		);

		$styleConfiguration = { ...$styleConfiguration };

		refresh = false;
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
		scale={1.4}
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
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							logoImage = e.detail.value;
							if (logoImage && typeof logoImage !== 'string') {
								// @ts-ignore
								convertBlobToBase64(logoImage.src).then((value) => {
									if (value) $styleConfiguration.eyegway.logo = value;
								});
							}

							logoImage = $styleConfiguration.eyegway.logo;

							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={schemeRGB}
					label="Main Accent Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							schemeRGB = e.detail.value;
							const out = RGBToHSLString(schemeRGB.r, schemeRGB.g, schemeRGB.b);
							$styleConfiguration.bulma.scheme = { h: out.h, s: out.s, main_l: out.l };

							schemeRGB = HSLStringToRGB(
								$styleConfiguration.bulma.scheme.h,
								$styleConfiguration.bulma.scheme.s,
								$styleConfiguration.bulma.scheme.main_l
							);
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleConfiguration.eyegway.header['background-color']}
					label="Header Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleConfiguration.eyegway.panel['background-color']}
					label="Panel Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleConfiguration.eyegway.content['background-color']}
					label="Content Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleConfiguration.eyegway.background['first-color']}
					label="Internal Body Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleConfiguration.eyegway.background['second-color']}
					label="External Body Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Separator />
				<Slider
					bind:value={borderLPercent}
					min={0}
					max={100}
					label="Border Brightness"
					format={(v) => v.toFixed(0)}
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							borderLPercent = e.detail.value;
							$styleConfiguration.bulma.border_l = borderLPercent + '%';

							borderLPercent = removePercent($styleConfiguration.bulma.border_l);
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Slider
					bind:value={textLPercent}
					min={0}
					max={100}
					label="Text Brightness"
					format={(v) => v.toFixed(0)}
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							textLPercent = e.detail.value;
							$styleConfiguration.bulma.text_l = textLPercent + '%';
							$styleConfiguration.bulma.text_strong_l = textLPercent + 19 + '%';
							$styleConfiguration.bulma.text_weak_l = textLPercent - 8 + '%';

							textLPercent = removePercent($styleConfiguration.bulma.text_l);
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
				<Slider
					bind:value={shadowLPercent}
					min={0}
					max={100}
					label="Shadow Brightness"
					format={(v) => v.toFixed(0)}
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							shadowLPercent = e.detail.value;
							$styleConfiguration.bulma.shadow_l = shadowLPercent + '%';

							shadowLPercent = removePercent($styleConfiguration.bulma.shadow_l);
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
			</TabPage>
			<TabPage title="Buttons">
				<Color
					bind:value={primaryRGB}
					label="Primary Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							primaryRGB = e.detail.value;
							const out = RGBToHSLString(primaryRGB.r, primaryRGB.g, primaryRGB.b);
							$styleConfiguration.bulma.primary = { h: out.h, s: out.s, l: out.l };

							primaryRGB = HSLStringToRGB(
								$styleConfiguration.bulma.primary.h,
								$styleConfiguration.bulma.primary.s,
								$styleConfiguration.bulma.primary.l
							);
						}
					}}
				/>
				<Color
					bind:value={infoRGB}
					label="Info Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							infoRGB = e.detail.value;
							const out = RGBToHSLString(infoRGB.r, infoRGB.g, infoRGB.b);
							$styleConfiguration.bulma.info = { h: out.h, s: out.s, l: out.l };

							infoRGB = HSLStringToRGB(
								$styleConfiguration.bulma.info.h,
								$styleConfiguration.bulma.info.s,
								$styleConfiguration.bulma.info.l
							);
						}
					}}
				/>
				<Color
					bind:value={linkRGB}
					label="Link Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							linkRGB = e.detail.value;
							const out = RGBToHSLString(linkRGB.r, linkRGB.g, linkRGB.b);
							$styleConfiguration.bulma.link = { h: out.h, s: out.s, l: out.l };

							linkRGB = HSLStringToRGB(
								$styleConfiguration.bulma.link.h,
								$styleConfiguration.bulma.link.s,
								$styleConfiguration.bulma.link.l
							);
						}
					}}
				/>
				<Color
					bind:value={successRGB}
					label="Success Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							successRGB = e.detail.value;
							const out = RGBToHSLString(successRGB.r, successRGB.g, successRGB.b);
							$styleConfiguration.bulma.success = { h: out.h, s: out.s, l: out.l };

							successRGB = HSLStringToRGB(
								$styleConfiguration.bulma.success.h,
								$styleConfiguration.bulma.success.s,
								$styleConfiguration.bulma.success.l
							);
						}
					}}
				/>
				<Color
					bind:value={warningRGB}
					label="Warning Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							warningRGB = e.detail.value;
							const out = RGBToHSLString(warningRGB.r, warningRGB.g, warningRGB.b);
							$styleConfiguration.bulma.warning = { h: out.h, s: out.s, l: out.l };

							warningRGB = HSLStringToRGB(
								$styleConfiguration.bulma.warning.h,
								$styleConfiguration.bulma.warning.s,
								$styleConfiguration.bulma.warning.l
							);
						}
					}}
				/>
				<Color
					bind:value={dangerRGB}
					label="Danger Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							dangerRGB = e.detail.value;
							const out = RGBToHSLString(dangerRGB.r, dangerRGB.g, dangerRGB.b);
							$styleConfiguration.bulma.danger = { h: out.h, s: out.s, l: out.l };

							dangerRGB = HSLStringToRGB(
								$styleConfiguration.bulma.danger.h,
								$styleConfiguration.bulma.danger.s,
								$styleConfiguration.bulma.danger.l
							);
							$styleConfiguration.id = Date.now();
						}
					}}
				/>
			</TabPage>
		</TabGroup>
	</Pane>
{/if}
