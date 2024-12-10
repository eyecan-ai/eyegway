<script lang="ts">
	import {
		Color,
		Pane,
		Image,
		type ImageValue,
		Slider,
		Separator,
		TabGroup,
		TabPage
	} from 'svelte-tweakpane-ui';
	import { styleSettings } from './SettingsStore.js';
	import {
		HSLStringToRGB,
		RGBToHSLString,
		removePercent,
		convertBlobToBase64
	} from './StyleSettingsUtils.js';
	import { onMount } from 'svelte';

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
		logoImage = $styleSettings.eyegway.logo;

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

		$styleSettings = { ...$styleSettings };

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
									if (value) $styleSettings.eyegway.logo = value;
								});
							}

							logoImage = $styleSettings.eyegway.logo;

							$styleSettings.id = Date.now();
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
							$styleSettings.bulma.scheme = { h: out.h, s: out.s, main_l: out.l };

							schemeRGB = HSLStringToRGB(
								$styleSettings.bulma.scheme.h,
								$styleSettings.bulma.scheme.s,
								$styleSettings.bulma.scheme.main_l
							);
							$styleSettings.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleSettings.eyegway.header['background-color']}
					label="Header Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleSettings.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleSettings.eyegway.panel['background-color']}
					label="Panel Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleSettings.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleSettings.eyegway.content['background-color']}
					label="Content Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleSettings.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleSettings.eyegway.background['first-color']}
					label="Internal Body Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleSettings.id = Date.now();
						}
					}}
				/>
				<Color
					bind:value={$styleSettings.eyegway.background['second-color']}
					label="External Body Background Color"
					on:change={(e) => {
						if (e.detail.origin === 'internal') {
							$styleSettings.id = Date.now();
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
							$styleSettings.bulma.border_l = borderLPercent + '%';

							borderLPercent = removePercent($styleSettings.bulma.border_l);
							$styleSettings.id = Date.now();
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
							$styleSettings.bulma.text_l = textLPercent + '%';
							$styleSettings.bulma.text_strong_l = textLPercent + 19 + '%';
							$styleSettings.bulma.text_weak_l = textLPercent - 8 + '%';

							textLPercent = removePercent($styleSettings.bulma.text_l);
							$styleSettings.id = Date.now();
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
							$styleSettings.bulma.shadow_l = shadowLPercent + '%';

							shadowLPercent = removePercent($styleSettings.bulma.shadow_l);
							$styleSettings.id = Date.now();
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
							$styleSettings.bulma.primary = { h: out.h, s: out.s, l: out.l };

							primaryRGB = HSLStringToRGB(
								$styleSettings.bulma.primary.h,
								$styleSettings.bulma.primary.s,
								$styleSettings.bulma.primary.l
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
							$styleSettings.bulma.info = { h: out.h, s: out.s, l: out.l };

							infoRGB = HSLStringToRGB(
								$styleSettings.bulma.info.h,
								$styleSettings.bulma.info.s,
								$styleSettings.bulma.info.l
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
							$styleSettings.bulma.link = { h: out.h, s: out.s, l: out.l };

							linkRGB = HSLStringToRGB(
								$styleSettings.bulma.link.h,
								$styleSettings.bulma.link.s,
								$styleSettings.bulma.link.l
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
							$styleSettings.bulma.success = { h: out.h, s: out.s, l: out.l };

							successRGB = HSLStringToRGB(
								$styleSettings.bulma.success.h,
								$styleSettings.bulma.success.s,
								$styleSettings.bulma.success.l
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
							$styleSettings.bulma.warning = { h: out.h, s: out.s, l: out.l };

							warningRGB = HSLStringToRGB(
								$styleSettings.bulma.warning.h,
								$styleSettings.bulma.warning.s,
								$styleSettings.bulma.warning.l
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
							$styleSettings.bulma.danger = { h: out.h, s: out.s, l: out.l };

							dangerRGB = HSLStringToRGB(
								$styleSettings.bulma.danger.h,
								$styleSettings.bulma.danger.s,
								$styleSettings.bulma.danger.l
							);
							$styleSettings.id = Date.now();
						}
					}}
				/>
			</TabPage>
		</TabGroup>
	</Pane>
{/if}
