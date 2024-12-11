<script lang="ts">
	import { slide } from 'svelte/transition';
	import { EllipsisVertical, Download, Upload, RefreshCcwDot, Library } from 'lucide-svelte';
	import type { ConfigurationUtils } from './ConfigurationUtils.js';
	import { createEventDispatcher, onMount } from 'svelte';

	export let config: ConfigurationUtils<any>;

	const dispatch = createEventDispatcher();

	let showDropdown = false;

	let configOptions: string[] = [];
	let activeOption: string = '';

	let dropdownRef: HTMLDivElement;

	onMount(async () => {
		configOptions = (await config.getOptions()) || [];
		activeOption = (await config.getActiveOption()) || '';
	});

	function handleClickOutside(event: MouseEvent) {
		if (dropdownRef && !dropdownRef.contains(event.target as Node)) {
			showDropdown = false;
		}
	}

	$: {
		if (showDropdown) {
			document.addEventListener('mousedown', handleClickOutside);
		} else {
			document.removeEventListener('mousedown', handleClickOutside);
		}
	}
</script>

<div transition:slide={{ axis: 'x' }} class="columns is-vcentered is-variable is-1 is-mobile">
	<div class="column is-narrow">
		<EllipsisVertical size={16} />
	</div>
	<div class="column is-narrow">
		<!-- SAVE TO FILE-->
		<button
			class="button is-small is-info is-outlined"
			on:click={() => {
				config.saveConfigurationToFile();
			}}
			title="Save Configuration to File"
		>
			<Download strokeWidth={2} size={16} />
		</button>
	</div>
	<div class="column is-narrow">
		<!-- LOAD FROM FILE-->
		<button
			class="button is-small is-info is-outlined"
			on:click={() => {
				config.loadConfigurationFromFile().then(() => {
					dispatch('update');
				});
			}}
			title="Load Configuration from File"
		>
			<Upload strokeWidth={2} size={16} />
		</button>
	</div>
	<div class="column is-narrow">
		<!-- LOAD PREDEFINED -->
		<div class="dropdown is-up {showDropdown ? 'is-active' : ''}" bind:this={dropdownRef}>
			<div class="dropdown-trigger">
				<button
					class="button is-small is-success is-outlined"
					on:click={() => {
						config.getActiveOption().then((active) => {
							activeOption = active;
						});
						showDropdown = !showDropdown;
					}}
					aria-haspopup="true"
					aria-controls="dropdown-menu"
					title="Load Predefined Theme"
				>
					<Library strokeWidth={2} size={16} />
				</button>
			</div>
			<div class="dropdown-menu" id="dropdown-menu" role="menu">
				<div class="dropdown-content">
					{#if configOptions.length > 0}
						{#if activeOption == ''}
							<a href={'#'} class="dropdown-item has-text-weight-bold is-active"> custom </a>
						{/if}
						{#each configOptions as option}
							<a
								href={'#'}
								class="dropdown-item has-text-weight-bold"
								class:is-active={option === activeOption}
								on:click|preventDefault={() => {
									config.loadConfigurationFromOptions(option).then(() => {
										showDropdown = false;
										dispatch('update');
									});
								}}
							>
								{option.split('/').pop()?.replace('.json', '').replace(/_/g, ' ')}
							</a>
						{/each}
					{:else}
						<div class="dropdown-item has-text-weight-bold">No options available</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
	<div class="column is-narrow">
		<!-- CLEAR LAYOUT -->
		<button
			class="button is-small is-danger is-outlined"
			on:click={() => {
				config.resetStore();
				dispatch('update');
			}}
			title="Reset to Default"
		>
			<RefreshCcwDot strokeWidth={2} size={16} />
		</button>
	</div>
</div>
