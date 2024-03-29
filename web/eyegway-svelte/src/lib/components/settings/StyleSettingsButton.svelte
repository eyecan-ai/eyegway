<script lang="ts">
	import { IconPalette } from '@tabler/icons-svelte';
	import StyleSettingsPanel from './StyleSettingsPanel.svelte';

	export let direction: string = 'left';
	export let up: boolean = true;
</script>

<div class="dropdown is-hoverable is-{direction}" class:is-up={up}>
	<div class="dropdown-trigger">
		<button class="button is-small is-warning" aria-haspopup="true" aria-controls="dropdown-menu4">
			<IconPalette />
		</button>
	</div>
	<div class="dropdown-menu" id="dropdown-menu4" role="menu">
		<div class="dropdown-contentx">
			<StyleSettingsPanel />
		</div>
	</div>
</div>
