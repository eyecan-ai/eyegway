<script lang="ts">
    import type { DataImage } from '../PaneModel.js';
    import type { ImageSettings } from '../settings/SettingsModel.js';

    export let userData: DataImage | null = null;
    export let userSettings: ImageSettings | null = null;
</script>

{#if userData && userSettings}
    <div class="image-container">
        <img 
            src={userData.url}
            alt="Something went wrong."
            style="object-fit: {userSettings.fit};"
        />
    </div>
{/if}

<style>
    .image-container {
        border-radius: 10px;
        overflow: hidden; 
        width: 100%;
        height: 100%;
        position: relative;
    }

    .image-container img {
        width: 100%;
        height: 100%;
        display: block;
        object-position: center;
    }
</style>