<script lang="ts">
	import { slide } from 'svelte/transition';
	import { EllipsisVertical, Download, Upload, RefreshCcwDot, Library } from 'lucide-svelte';
	import type { ConfigurationUtils } from './ConfigurationUtils.js';

	export let config: ConfigurationUtils<any>;

	let showDropdown = false;

	async function fetchOptions() {
		const configOptions = await config.getOptions();
		const activeOption = await config.getActiveOption();
		return { configOptions, activeOption };
	}

	function toggleDropdown() {
		showDropdown = !showDropdown;
	}

	function selectTheme(option: string) {
		config.loadConfigurationFromOptions(option);
		showDropdown = false;
	}
</script>

<div transition:slide={{ axis: 'x' }} class="columns is-vcentered is-variable is-1">
	<div class="column is-narrow">
		<EllipsisVertical size={16} />
	</div>
	<div class="column is-narrow">
		<!-- SAVE TO FILE-->
		<button
			class="button is-small is-info is-outlined"
			on:click={() => config.saveConfigurationToFile()}
			title="Save Configuration to File"
		>
			<Download strokeWidth={2} size={16} />
		</button>
	</div>
	<div class="column is-narrow">
		<!-- LOAD FROM FILE-->
		<button
			class="button is-small is-info is-outlined"
			on:click={() => config.loadConfigurationFromFile()}
			title="Load Configuration from File"
		>
			<Upload strokeWidth={2} size={16} />
		</button>
	</div>
	<div class="column is-narrow">
		<!-- LOAD PREDEFINED -->
		<div class="dropdown is-up {showDropdown ? 'is-active' : ''}">
			<div class="dropdown-trigger">
				<button
					class="button is-small is-success is-outlined"
					on:click={toggleDropdown}
					aria-haspopup="true"
					aria-controls="dropdown-menu"
					title="Load Predefined Theme"
				>
					<Library strokeWidth={2} size={16} />
				</button>
			</div>
			<div class="dropdown-menu" id="dropdown-menu" role="menu">
				{#if showDropdown}
					{#await fetchOptions()}
						<div class="dropdown-content">
							<div class="dropdown-item">Loading...</div>
						</div>
					{:then { configOptions, activeOption }}
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
										on:click|preventDefault={() => selectTheme(option)}
									>
										{option.split('/').pop()?.replace('.json', '').replace(/_/g, ' ')}
									</a>
								{/each}
							{:else}
								<div class="dropdown-item has-text-weight-bold">No options available</div>
							{/if}
						</div>
					{/await}
				{/if}
			</div>
		</div>
	</div>
	<div class="column is-narrow">
		<!-- CLEAR LAYOUT -->
		<button
			class="button is-small is-danger is-outlined"
			on:click={() => {
				config.resetStore();
			}}
			title="Reset to Default"
		>
			<RefreshCcwDot strokeWidth={2} size={16} />
		</button>
	</div>
</div>
