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
        /* "position: absolute" makes the image to behave as the background
           of its container, without changing the size of the container itself */
        position: absolute; 
        top: 0;
        left: 0;

        /* fill the container, but keep the aspect ratio of the image */
        width: 100%;
        height: 100%;

        /* center the image in the container */
        object-position: center;
    }
</style>