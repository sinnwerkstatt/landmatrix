<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet" />
</svelte:head>

<h1>I am part of the layout</h1>
<hr>

<slot />

<style>
    :global(body) {
        @apply font-inter font-semibold text-a-sm;
    }
</style>