<script lang="ts">
	import PaneNode from './PaneNode.svelte';
	import StyleSettingsButton from '../settings/StyleSettingsButton.svelte';
	import { EllipsisVertical, Download, Upload, Edit, Save, History } from 'lucide-svelte';
	import { PaneConfiguration } from './PaneModel.js';
	import { PaneConfigurationUtils } from './PaneUtils.js';
	import { onMount } from 'svelte';

	// State variables
	export let editMode: boolean = true;
	export let dataStream: any = {};
	export let autoLoadDefault: boolean = true;

	let disabled = false;

	// Initialize root pane
	let rootPane: PaneConfiguration = {
		id: Date.now(),
		split: '',
		size: 100,
		children: [],
		item: { name: '' }
	};

	onMount(() => {
		if (autoLoadDefault) {
			loadDefaultConfiguration();
		}
	});

	/**
	 * Export the current configuration. It can be called from the parent component.
	 */
	export function exportConfiguration(): PaneConfiguration {
		const configuration = rootPane;
		return configuration;
	}

	/**
	 * Save the configuration to a file. It can be called from the parent component.
	 */
	export function saveConfigurationToFile() {
		const configuration = exportConfiguration();
		PaneConfigurationUtils.saveConfigurationToFile(configuration);
	}

	/**
	 * Load the configuration from a file. It can be called from the parent component.
	 */
	export async function loadConfigurationFromFile() {
		const configuration = await PaneConfigurationUtils.loadConfigurationFromFile();
		reloadConfiguration(configuration);
	}

	/**
	 * Save the configuration as default. It can be called from the parent component.
	 */
	export function saveConfigurationAsDefault() {
		const configuration = exportConfiguration();
		PaneConfigurationUtils.saveConfigurationAsDefault(configuration);
	}

	/**
	 * Load the default configuration. It can be called from the parent component.
	 */
	export function loadDefaultConfiguration() {
		const configuration = PaneConfigurationUtils.loadDefaultConfiguration();
		if (configuration) reloadConfiguration(configuration);
	}

	/**
	 * Reload the configuration. It can be called from the parent component.
	 */
	export function reloadConfiguration(configuration: PaneConfiguration) {
		disabled = true;
		rootPane = configuration;
		setTimeout(() => {
			disabled = false;
		}, 100);
	}

	// Controls visibility
	let controls = true;

	// Functions to manage panes
	function toggleEditMode() {
		editMode = !editMode;
	}

	// Handle deletePane event from PaneNode
	function handleDeletePane(event: CustomEvent) {
		const paneToDelete = event.detail.pane;
		removePane(rootPane, paneToDelete);
	}

	// Recursive function to remove a pane from the tree
	function removePane(parentPane: PaneConfiguration, paneToDelete: PaneConfiguration) {
		if (!parentPane.children) return false;

		const index = parentPane.children.findIndex((child) => child.id === paneToDelete.id);
		if (index !== -1) {
			parentPane.children.splice(index, 1);
			if (parentPane.children.length === 1) {
				// Collapse parent pane if only one child remains
				const remainingChild = parentPane.children[0];
				parentPane.split = remainingChild.split;
				parentPane.children = remainingChild.children;
				parentPane.item = remainingChild.item;
			} else if (parentPane.children.length === 0) {
				parentPane.split = '';
				parentPane.item = { name: '' };
			}
			return true;
		}

		// Recursively search in child panes
		for (let child of parentPane.children) {
			if (removePane(child, paneToDelete)) {
				return true;
			}
		}

		return false;
	}
</script>

<div class="mosaic">
	<div class="is-flex p-0 is-align-items-center is-justify-content-center" style="height: 100%">
		{#if !editMode}
			{#if !rootPane || (!rootPane.split && !rootPane.item.name)}
				<div class="notification m-4 no-items">No items, add one ...</div>
			{/if}
		{/if}
		<!-- Render the root pane node -->
		<PaneNode
			pane={rootPane}
			{editMode}
			{dataStream}
			tips={dataStream ? Object.keys(dataStream) : []}
			on:deletePane={handleDeletePane}
		/>
	</div>

	{#if controls}
		<div class="controls p-2" class:controls-hidden={!editMode}>
			<div class="columns is-vcentered is-variable is-1">
				<div class="column is-narrow">
					<StyleSettingsButton />
				</div>
				<div class="column is-narrow">
					<button
						class="button is-warning is-small"
						class:is-inverted={editMode}
						on:click={toggleEditMode}
						title="{editMode ? 'Disable' : 'Enable'} Edit Mode"
					>
						<Edit size={16} />
					</button>
				</div>
				{#if editMode}
					<div class="column is-narrow">
						<EllipsisVertical size={16} />
					</div>
					<div class="column is-narrow">
						<!-- SAVE TO FILE-->
						<button
							class="button is-small is-info is-inverted"
							on:click={saveConfigurationToFile}
							title="Download current Configuration to File"
						>
							<Download strokeWidth={1} size={18} />
						</button>

						<!-- LOAD FROM FILE-->
						<button
							class="button is-small is-inverted is-info"
							on:click={loadConfigurationFromFile}
							title="Load Configuration from File"
						>
							<Upload strokeWidth={1} size={18} />
						</button>

						<!-- SAVE AS DEFAULT-->
						<button
							class="button is-small is-inverted is-info"
							on:click={saveConfigurationAsDefault}
							title="Save as Default Configuration"
						>
							<Save strokeWidth={1} size={18} />
						</button>

						<!-- LOAD DEFAULT-->
						<button
							class="button is-small is-inverted is-info"
							on:click={loadDefaultConfiguration}
							title="Reload Default Configuration"
						>
							<History strokeWidth={1} size={18} />
						</button>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.no-items {
		margin-top: 100px;
		position: absolute;
	}
	.mosaic {
		height: 100%;
		padding: 5px !important;
	}
	.mosaic .controls-hidden {
		display: none;
	}
	.mosaic:hover .controls-hidden {
		display: block;
	}
	.controls {
		margin-top: 4px;
	}
</style>
