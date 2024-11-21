<script lang="ts">
	import PaneNode from './PaneNode.svelte';
	import StyleSettingsPanel from './settings/StyleSettingsPanel.svelte';
	import { Edit, Palette } from 'lucide-svelte';
	import {
		paneConfiguration,
		savePaneConfigurationToFile,
		loadPaneConfigurationFromFile,
		paneConfigurationReset
	} from './PaneStore.js';
	import {
		saveStyleSettingsToFile,
		loadStyleSettingsFromFile,
		styleSettingsReset
	} from './settings/SettingsStore.js';
	import SerializationControls from '../utils/SerializationControls.svelte';

	// State variables
	export let editMode: boolean = true;
	export let styleMode: boolean = false;
	export let dataStream: any = {};
	export let controls = true;

	// Functions to manage panes
	function toggleEditMode() {
		editMode = !editMode;
	}
	function toggleStyleMode() {
		styleMode = !styleMode;
	}
</script>

<div class="panels">
	<div class="is-flex p-0 is-align-items-center is-justify-content-center" style="height: 100%">
		{#if !editMode}
			{#if !$paneConfiguration || (!$paneConfiguration.split && !$paneConfiguration.item?.name)}
				<div class="notification m-4 no-items">No items, add one ...</div>
			{/if}
		{/if}
		<PaneNode
			bind:pane={$paneConfiguration}
			{editMode}
			{dataStream}
			tips={dataStream ? Object.keys(dataStream) : []}
		/>
		<StyleSettingsPanel isDisabled={!styleMode} />
	</div>

	{#if controls}
		<div class="controls p-2" class:controls-hidden={!editMode && !styleMode}>
			<div class="columns is-vcentered is-variable is-1">
				<div class="column is-narrow">
					<button
						class="button is-warning is-small"
						disabled={editMode}
						class:is-inverted={styleMode}
						on:click={toggleStyleMode}
						title="{styleMode ? 'Disable' : 'Enable'} Edit Mode"
					>
						<Palette size={16} />
					</button>
				</div>
				<div class="column is-narrow">
					<button
						class="button is-warning is-small"
						disabled={styleMode}
						class:is-inverted={editMode}
						on:click={toggleEditMode}
						title="{editMode ? 'Disable' : 'Enable'} Edit Mode"
					>
						<Edit size={16} />
					</button>
				</div>
				{#if styleMode}
					<SerializationControls
						saveConfigurationToFile={saveStyleSettingsToFile}
						loadConfigurationFromFile={loadStyleSettingsFromFile}
						configurationReset={styleSettingsReset}
					/>
				{/if}
				{#if editMode}
					<SerializationControls
						saveConfigurationToFile={savePaneConfigurationToFile}
						loadConfigurationFromFile={loadPaneConfigurationFromFile}
						configurationReset={paneConfigurationReset}
					/>
				{/if}
			</div>
		</div>
	{/if}
</div>

<style>
	.panels {
		height: 100%;
		padding: 5px !important;
	}
	.panels .controls-hidden {
		display: none;
	}
	.panels:hover .controls-hidden {
		display: block;
	}
	.controls {
		margin-top: 4px;
	}
</style>
