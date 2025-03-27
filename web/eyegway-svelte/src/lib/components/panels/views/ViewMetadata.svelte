<script lang="ts">
	import { JSONEditor, Mode } from 'svelte-jsoneditor';
	import type { DataMetadata } from '../PaneModel.js';
	import type { MetadataSettings } from '../settings/SettingsModel.js';

	export let userData: DataMetadata | null = null;
	export let userSettings: MetadataSettings | null = null;
</script>

{#if userData && userSettings}
    <div class="my-json-editor">
        <JSONEditor
            content={{ json: userData.data }}
            mode={Mode[userSettings.mode]}
            mainMenuBar={false}
            navigationBar={false}
            statusBar={false}
            readOnly
        />
    </div>
{/if}

<style>
	.my-json-editor {
		--jse-main-border: 'transparent';
		--jse-background-color: 'transparent';
		--jse-text-color: var(--bulma-text);
		--jse-text-readonly: var(--bulma-text);
		--jse-key-color: var(--bulma-text);
		--jse-value-color: var(--bulma-primary);
		--jse-value-color-number: var(--bulma-success);
		--jse-value-color-boolean: var(--bulma-danger);
		--jse-value-color-null: var(--bulma-warning);
		--jse-value-color-string: var(--bulma-info);
		--jse-value-color-url: var(--bulma-link);
        overflow: auto;
	}
</style>
