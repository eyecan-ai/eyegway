<script lang="ts">
	import { Palette } from 'lucide-svelte';
	import StyleSettingsPanel from './StyleSettingsPanel.svelte';

	export let direction: string = 'left';
	export let up: boolean = true;
	let hovering: boolean = false;
</script>

<div class="dropdown is-hoverable is-{direction}" class:is-up={up}>
	<div class="dropdown-trigger">
		<button class="button is-small is-warning" aria-haspopup="true" aria-controls="dropdown-menu4">
			<Palette size={18} />
		</button>
	</div>
	<div class="dropdown-menu" id="dropdown-menu4" role="menu">
		<div class="dropdown-contentx">
			<StyleSettingsPanel />
		</div>
	</div>
</div>

<style>
	button {
		transition: all 0.3s;
		border-radius: 0;
	}
	button:hover {
		border-radius: 0 50% 0 0 !important;
	}
</style>
