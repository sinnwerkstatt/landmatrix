<script lang="ts">
    import Navbar from "$components/Accountability/Navbar.svelte"
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet" />
</svelte:head>

<div class="h-screen flex flex-row flex-nowrap bg-a-gray-100">
    <Navbar />
    <slot />
</div>

<style>
    /* Global Accountability styles */
    :global(body) {
        @apply font-inter font-medium text-a-sm text-a-gray-900;
    }
</style>