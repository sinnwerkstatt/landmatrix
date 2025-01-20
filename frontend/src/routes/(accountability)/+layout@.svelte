<script lang="ts">
  import Navbar from "$components/Accountability/Navbar.svelte"

  interface Props {
    children?: import("svelte").Snippet
  }

  let { children }: Props = $props()
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap"
    rel="stylesheet"
  />
</svelte:head>

<div class="flex h-screen flex-row flex-nowrap bg-a-gray-100">
  <Navbar />
  {@render children?.()}
</div>

<style>
  /* Global Accountability styles */
  :global {
    body {
      @apply font-inter text-a-sm font-medium text-a-gray-900;
    }

    h1,
    h2,
    h3,
    div {
      @apply text-a-gray-900;
    }

    a.link,
    a.link:hover {
      @apply text-a-sm font-medium text-a-gray-900 underline underline-offset-4;
    }
    ::-webkit-scrollbar {
      @apply w-1;
      @apply rounded-full;
    }
    ::-webkit-scrollbar-track {
      @apply rounded-full bg-a-gray-200;
    }
    ::-webkit-scrollbar-thumb {
      @apply rounded-full bg-a-gray-800;
    }
  }
</style>
