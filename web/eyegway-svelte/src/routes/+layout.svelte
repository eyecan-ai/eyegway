<script lang="ts">
	import { Parameters } from '$lib/Parameters.js';
	const title = Parameters.title;
</script>

<svelte:head>
	<title>{title}</title>
</svelte:head>
<slot />
